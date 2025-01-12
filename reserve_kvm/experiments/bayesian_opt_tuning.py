from ray import tune
from ray.tune.tuner import Tuner
from ray.tune.search.bayesopt import BayesOptSearch
from ray.air import RunConfig
from common import svm_train

# Bayesian Optimization Configuration
bayes_search_config = {
    "kernel": tune.choice(["linear", "rbf", "poly"]),
    "C": tune.loguniform(0.1, 10),
    "gamma": tune.loguniform(0.01, 1),  # Only for non-linear kernels
    "degree": tune.choice([2, 3, 4])  # Only for poly kernel
}

# Initialize Bayesian Optimization
bayesopt_search = BayesOptSearch(metric="mean_loss", mode="min")

# Run Bayesian Optimization
tuner = Tuner(
    svm_train,
    param_space=bayes_search_config,
    tune_config=tune.TuneConfig(
        search_alg=bayesopt_search,
        num_samples=50
    ),
    run_config=RunConfig(
        name="bayesian_opt_svm",
        storage_path="./ray_results"
    )
)

# Run the tuning job
results = tuner.fit()

# Print the best hyperparameters
best_result = results.get_best_result(metric="mean_loss", mode="min")
print("Best hyperparameters:", best_result.config)
