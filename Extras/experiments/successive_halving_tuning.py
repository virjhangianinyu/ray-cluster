from ray import tune
from ray.tune.tuner import Tuner
from ray.tune.schedulers import ASHAScheduler
from ray.air import RunConfig
from svm_trainer import svm_train

# Successive Halving Configuration
asha_scheduler = ASHAScheduler(
    metric="mean_loss",
    mode="min",
    grace_period=1,
    reduction_factor=2
)

asha_search_config = {
    "kernel": tune.choice(["linear", "rbf", "poly"]),
    "C": tune.loguniform(0.1, 10),
    "gamma": tune.loguniform(0.01, 1),  # Only for non-linear kernels
    "degree": tune.choice([2, 3, 4])  # Only for poly kernel
}

# Run Successive Halving
tuner = Tuner(
    svm_train,
    param_space=asha_search_config,
    tune_config=tune.TuneConfig(
        num_samples=50,  # Total trials
        scheduler=asha_scheduler
    ),
    run_config=RunConfig(
        name="successive_halving_svm",
        storage_path="./ray_results"
    )
)

# Run the tuning job
results = tuner.fit()

# Print the best hyperparameters
best_result = results.get_best_result(metric="mean_loss", mode="min")
print("Best hyperparameters:", best_result.config)
