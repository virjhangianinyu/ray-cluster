from ray import tune
from ray.tune.tuner import Tuner
from ray.air import RunConfig
from svm_trainer import svm_train

# Random Search Configuration
random_search_config = {
    "kernel": tune.choice(["linear", "rbf", "poly"]),
    "C": tune.loguniform(0.1, 10),
    "gamma": tune.loguniform(0.01, 1),  # Only for non-linear kernels
    "degree": tune.choice([2, 3, 4])  # Only for poly kernel
}

# Run Random Search
tuner = Tuner(
    svm_train,
    param_space=random_search_config,
    tune_config=tune.TuneConfig(num_samples=50),  # Randomly sample 50 configurations
    run_config=RunConfig(
        name="random_search_svm",
        storage_path="./ray_results"
    )
)

# Run the tuning job
results = tuner.fit()

# Print the best hyperparameters
best_result = results.get_best_result(metric="mean_loss", mode="min")
print("Best hyperparameters:", best_result.config)
