from ray.air import session
from ray import tune
from ray.tune.tuner import Tuner
from ray.air import RunConfig
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import ray

# SVM Training Function
def svm_train(config):
    digits = load_digits()
    X, y = digits.data, digits.target
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = SVC(kernel=config["kernel"], C=config["C"], gamma=config.get("gamma", "scale"))
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)
    session.report({"mean_loss": -accuracy})

# Grid Search Configuration
grid_search_config = {
    "kernel": tune.grid_search(["linear", "rbf"]),
    "C": tune.grid_search([0.1, 1, 10]),
    "gamma": tune.grid_search([0.01, 0.1, 1])  # Only relevant for rbf
}

ray.init(address="auto")

tuner = Tuner(
    svm_train,
    param_space=grid_search_config,
    tune_config=tune.TuneConfig(num_samples=1),
    run_config=RunConfig(
        name="grid_search_svm",
        storage_path="file:///home/cc/.ray_results"
    )
)

results = tuner.fit()
best_result = results.get_best_result(metric="mean_loss", mode="min")
print("Best hyperparameters:", best_result.config)
