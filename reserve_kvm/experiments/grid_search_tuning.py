import ray
from ray.air import session
from ray import tune
from ray.tune.tuner import Tuner
from ray.air import RunConfig
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import hinge_loss, accuracy_score
import torch
from torchvision import datasets, transforms

# Initialize Ray (connect to Ray cluster)
ray.init(address="auto")

# Load MNIST dataset using PyTorch
def load_mnist():
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    mnist_train = datasets.MNIST(root="./data", train=True, download=False, transform=transform)
    X_train = mnist_train.data.numpy().reshape(-1, 28 * 28) / 255.0  # Normalize
    y_train = mnist_train.targets.numpy()
    return X_train, y_train

# SVM Training Function
def svm_train(config):
    # Load and preprocess MNIST
    X, y = load_mnist()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train the SVM
    model = SVC(kernel=config["kernel"], C=config["C"], gamma=config.get("gamma", "scale"))
    model.fit(X_train, y_train)

    # Calculate hinge loss on the validation set
    y_decision = model.decision_function(X_val)
    loss = hinge_loss(y_val, y_decision)

    # Report the loss for Ray Tune
    session.report({"loss": loss})

# Hyperparameter Configuration for Grid Search
grid_search_config = {
    "kernel": tune.grid_search(["linear", "rbf"]),
    "C": tune.grid_search([0.1, 1, 10]),
    "gamma": tune.grid_search([0.01, 0.1, 1])  # Only relevant for rbf kernel
}

# Tuner Setup
tuner = Tuner(
    svm_train,
    param_space=grid_search_config,
    tune_config=tune.TuneConfig(
        num_samples=1,  # Grid search tries all combinations
        metric="loss",  # Minimize the hinge loss
        mode="min"
    ),
    run_config=RunConfig(
        name="grid_search_mnist_svm",
        storage_path="file:///home/cc/.ray_results"  
    )
)

# Run the tuning job
results = tuner.fit()

# Get the best hyperparameters
best_result = results.get_best_result(metric="loss", mode="min")
print("Best hyperparameters:", best_result.config)

# Shutdown Ray after completion
ray.shutdown()
