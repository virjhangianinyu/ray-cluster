import ray
from ray import tune
from ray.tune.tuner import Tuner
from ray.tune.search.grid_search import GridSearch
from ray.tune.schedulers import ASHAScheduler
from ray.air import session, RunConfig
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models

# Define the training function
def train_cifar(config):
    # Dataset and preprocessing
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    train_dataset = datasets.CIFAR10(root="data", train=True, download=True, transform=transform)
    val_dataset = datasets.CIFAR10(root="data", train=False, download=True, transform=transform)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=int(config["batch_size"]), shuffle=True)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=int(config["batch_size"]), shuffle=False)

    # Model setup
    model = models.resnet18()
    model.fc = nn.Sequential(
        nn.Dropout(config["dropout"]),
        nn.Linear(model.fc.in_features, 10)
    )

    optimizer = optim.SGD(model.parameters(), lr=config["lr"])
    criterion = nn.CrossEntropyLoss()

    # Training loop
    for epoch in range(10):  # Train for 10 epochs
        model.train()
        for data, target in train_loader:
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

        # Validation accuracy
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data, target in val_loader:
                output = model(data)
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        accuracy = correct / total

        # Report accuracy after each epoch
        session.report({"accuracy": accuracy, "epoch": epoch})

# Define hyperparameter search space
search_space = {
    "lr": GridSearch([0.001, 0.01, 0.1]),
    "batch_size": GridSearch([64, 128, 256]),
    "dropout": GridSearch([0.2, 0.3, 0.5])
}

# Initialize Ray
ray.init(address="auto")

# Define the ASHA Scheduler
asha_scheduler = ASHAScheduler(
    metric="accuracy",
    mode="max",
    max_t=10,  # Maximum epochs
    grace_period=2,  # Minimum epochs before termination
    reduction_factor=2  # Halve the number of trials at each step
)

# Use Tuner for hyperparameter tuning
tuner = Tuner(
    train_cifar,
    param_space=search_space,
    tune_config=tune.TuneConfig(
        scheduler=asha_scheduler,  # Add ASHA scheduler
        num_samples=1,  # No random sampling since we're using GridSearch
        resources_per_trial={"cpu": 4}  # 1 CPU per trial
    ),
    run_config=RunConfig(
        storage_path="~/.ray_results",  # Replace with your preferred directory
        name="cifar10_tuning"  # Organize results under this name
    )
)

# Run the tuning job
results = tuner.fit()

# Print the best results
best_result = results.get_best_result(metric="accuracy", mode="max")
print("Best hyperparameters: ", best_result.config)

# Shutdown Ray
ray.shutdown()
