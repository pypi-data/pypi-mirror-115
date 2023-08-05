import logging
import multiprocessing
from datetime import datetime

import numpy as np
import pandas as pd
from tqdm import tqdm

from mmsbm.expectation_maximization import (
    normalize_with_d,
    init_random_array,
    normalize_with_self,
    update_coefficients,
    compute_likelihood,
    compute_prod_dist,
)
from mmsbm.data_handler import DataHandler
from mmsbm.utils import get_n_per_group, structure_folds


class MMSBM:
    data_handler = None
    results = None
    test = None
    theta = None
    eta = None
    pr = None
    likelihood = None
    prediction_matrix = None

    def __init__(
        self,
        user_groups,
        item_groups,
        iterations=400,
        sampling=1,
        seed=1714,
        debug=False,
    ):
        self.start_time = datetime.now()
        self.user_groups = user_groups
        self.item_groups = item_groups
        self.iterations = iterations
        self.sampling = sampling
        self.debug = debug

        # Initiate the random state
        rng = np.random.default_rng(seed)
        # Create seeds for each process
        self.seeds = list(rng.integers(low=1, high=10000, size=sampling))

        self.logger = logging.getLogger("MMSBM")
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    def _prepare_objects(self, train):

        # Create a few dicts with the relationships
        d0 = {}
        d1 = {}
        [d0.update({a: list(train[train[:, 0] == a, 1])}) for a in set(train[:, 0])]
        [d1.update({a: list(train[train[:, 1] == a, 0])}) for a in set(train[:, 1])]
        self.ratings = sorted(set(train[:, 2]))
        self.r = max(self.ratings)
        self.p = int(train[:, 0].max())
        self.m = int(train[:, 1].max())

        # If, for some reason, there are missing links, we need to fill them:
        [d0.update({a: []}) for a in set(range(self.p)).difference(set(d0.keys()))]
        [d1.update({a: []}) for a in set(range(self.m)).difference(set(d1.keys()))]

        self.train = train
        self.d0 = d0
        self.d1 = d1

    def fit(self, data, silent=False):

        if not silent:
            self.logger.info(
                f"Running {self.sampling} runs of {self.iterations} iterations."
            )

        # Get data
        self.data_handler = DataHandler()
        train = self.data_handler.format_train_data(data)
        self._prepare_objects(train)

        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        jobs = []
        for i in range(self.sampling):
            proc = multiprocessing.Process(
                target=self.run_one_sampling,
                args=(train, self.seeds[i], i, return_dict),
            )
            jobs.append(proc)
            proc.start()

        for proc in jobs:
            proc.join()

        self.results = return_dict

    def run_one_sampling(self, data, seed, i, return_dict):
        rng = np.random.default_rng(seed)

        # Generate random (but normalized) inits
        theta = normalize_with_d(
            init_random_array((self.p + 1, self.user_groups), rng), self.d0
        )
        eta = normalize_with_d(
            init_random_array((self.m + 1, self.item_groups), rng), self.d1
        )
        pr = normalize_with_self(
            init_random_array((self.user_groups, self.item_groups, self.r + 1), rng)
        )

        # Do the work
        # We store the prs to check convergence
        for j in tqdm(range(self.iterations)):
            # This is the crux of the script; please see funcs.py
            n_theta, n_eta, npr = update_coefficients(
                data=data, ratings=self.ratings, theta=theta, eta=eta, pr=pr
            )

            # Update with normalization
            theta = normalize_with_d(n_theta, self.d0)
            eta = normalize_with_d(n_eta, self.d1)
            pr = normalize_with_self(npr)

            if self.debug:
                # For debugging purposes; compute likelihood every once in a while
                if j % 50 == 0:
                    likelihood = compute_likelihood(
                        self.train, self.ratings, theta, eta, pr
                    )
                    self.logger.debug(
                        f"\nLikelihood at run {i} is {likelihood.sum():.0f}"
                    )

        likelihood = compute_likelihood(self.train, self.ratings, theta, eta, pr)

        return_dict[i] = {
            "likelihood": likelihood,
            "pr": pr,
            "theta": theta,
            "eta": eta,
        }

        return None

    def predict(self, data):

        test = self.data_handler.format_test_data(data)
        self.test = test

        # Get the info for all the runs
        rats = [
            compute_prod_dist(test, a["theta"], a["eta"], a["pr"])
            for a in self.results.values()
        ]
        prs = np.array([a["pr"] for a in self.results.values()])
        likelihoods = np.array([a["likelihood"] for a in self.results.values()])
        thetas = np.array([a["theta"] for a in self.results.values()])
        etas = np.array([a["eta"] for a in self.results.values()])

        best = self.choose_best_run(rats)

        # Store the cleaned best objects
        self.theta = self.data_handler.return_theta_indices(thetas[best])
        self.eta = self.data_handler.return_eta_indices(etas[best])
        self.pr = self.data_handler.return_pr_indices(prs[best])
        self.likelihood = likelihoods[best]

        # The prediction matrix is the average of all runs
        self.prediction_matrix = np.array(rats).mean(axis=0)

        return self.prediction_matrix

    def choose_best_run(self, rats):

        # We compute the accuracy of all of them and return the index of the best
        accuracies = [self._compute_stats(a)["accuracy"] for a in rats]
        return accuracies.index(max(accuracies))

    def score(self, silent=False):

        # Now average over rats to get a more robust prediction matrix and predict again
        stats = self._compute_stats(self.prediction_matrix)
        stats["likelihood"] = self.likelihood

        if not silent:
            # Explain how we did
            if self.debug:
                self.logger.info(
                    f"Done {self.sampling} runs in {(datetime.now() - self.start_time).total_seconds() / 60.0:.2f} "
                    f"minutes."
                )
            self.logger.info(
                f"The final accuracy is {stats['accuracy']}, the one off accuracy is {stats['one_off_accuracy']} "
                f"and the MAE is {stats['mae']}."
            )

        return {
            "stats": stats,
            "objects": {"theta": self.theta, "eta": self.eta, "pr": self.pr},
        }

    def _compute_stats(self, rat):
        # How did we do?
        rat = self._compute_indicators(rat)
        # Final model quality indicators
        stats = self._compute_final_stats(rat)

        return stats

    def _compute_indicators(self, rat):

        rat = pd.DataFrame(rat)
        rat["pred"] = np.argmax(rat.values, axis=1)

        # Add the real results
        rat = rat.assign(real=pd.Series(self.test[:, 2]))

        # Remove observations without predictions
        rat = rat.loc[rat.iloc[:, : len(self.ratings)].sum(axis=1) != 0, :]

        # Check the ones we got right
        rat["true"] = np.where(rat["pred"] == rat["real"], 1, 0)

        # Check the ones we got almost right
        rat["almost"] = np.where(abs(rat["pred"] - rat["real"]) <= 1, 1, 0)

        # squared error (which is not squared error but ok)
        rat["s2"] = abs(rat["pred"] - rat["real"])

        # Same but weighed
        # Note that we are assuming that weights are the first R columns
        rat["pred_pond"] = [
            self._weighting(a, self.ratings)
            for a in rat.iloc[:, : len(self.ratings)].values
        ]
        rat["true_pond"] = np.where(rat["real"] == round(rat["pred_pond"]), 1, 0)
        rat["s2pond"] = abs(rat["pred_pond"] - rat["real"])

        return rat

    @staticmethod
    def _compute_final_stats(rat):
        # Final model quality indicators
        accuracy = rat["true"].sum() / rat.shape[0]
        one_off_accuracy = rat["almost"].sum() / rat.shape[0]
        mae = 1 - rat["true_pond"].sum() / rat.shape[0]

        # Errors
        s2 = rat["s2"].sum()
        s2pond = rat["s2pond"].sum()

        return {
            "accuracy": accuracy,
            "one_off_accuracy": one_off_accuracy,
            "mae": mae,
            "s2": s2,
            "s2pond": s2pond,
        }

    @staticmethod
    def _weighting(x, ratings):
        return sum([a * b for (a, b) in zip(x, ratings)])

    def cv_fit(self, data, folds=5):

        accuracies = []

        items_per_fold = structure_folds(data, folds)

        temp = data
        all_results = []
        for f in range(folds):
            self.logger.info(f"Running fold {f + 1} of {folds}...")

            # Get the correct indices
            test_indices = [
                a
                for a in temp.groupby(temp.columns[0], as_index=False)
                .apply(get_n_per_group, n=items_per_fold)
                .values
            ]
            test_indices = [a for b in test_indices for a in b if str(a) != "0"]

            test = temp.loc[test_indices, :]
            train = data[~data.index.isin(test.index)]
            temp = temp[~temp.index.isin(test_indices)]

            self.fit(train, silent=True)
            self.prediction_matrix = self.predict(test)
            results = self.score(silent=True)

            # We put together the best run for each of the s samplings of each fold
            all_results.append(
                {
                    "stats": results["stats"],
                    "objects": {
                        "theta": self.theta,
                        "eta": self.eta,
                        "pr": self.pr,
                        "rat": self.prediction_matrix,
                    },
                }
            )
            accuracies.append(results["stats"]["accuracy"])

        # Now we pick the best objects
        accuracies = [a["stats"]["accuracy"] for a in all_results]
        best = accuracies.index(max(accuracies))
        self.theta = all_results[best]["objects"]["theta"]
        self.eta = all_results[best]["objects"]["eta"]
        self.pr = all_results[best]["objects"]["pr"]
        self.prediction_matrix = all_results[best]["objects"]["rat"]

        self.logger.info(f"Ran {folds} folds with accuracies {accuracies}.")
        self.logger.info(
            f"They have mean {np.mean(accuracies)} and sd {np.std(accuracies)}."
        )

        return accuracies
