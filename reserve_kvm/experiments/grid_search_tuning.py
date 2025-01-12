from ray import tune
from ray.tune.tuner import Tuner
from ray.air import RunConfig
from svm_trainer import svm_train

# Grid Search Configuration
grid_search_config = {
    "kernel": tune.grid_search(["linear", "rbf", "poly"]),
    "C": tune.grid_search([0.1, 1, 10]),
    "gamma": tune.grid_search([0.01, 0.1, 1]),
    "degree": tune.grid_search([2, 3, 4])  # Only for poly kernel
}

# Run Grid Search
tuner = Tuner(
    svm_train,
    param_space=grid_search_config,
    tune_config=tune.TuneConfig(num_samples=1),
    run_config=RunConfig(
        name="grid_search_svm",
        storage_path="./ray_results"
    )
)

# Run the tuning job
results = tuner.fit()

# Print the best hyperparameters
best_result = results.get_best_result(metric="mean_loss", mode="min")
print("Best hyperparameters:", best_result.config)
