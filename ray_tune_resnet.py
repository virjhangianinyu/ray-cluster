import ray
from ray import tune
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models

# Training function
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

    # Validation function
    def validate_model():
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data, target in val_loader:
                output = model(data)
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        return correct / total

    # Report validation accuracy
    accuracy = validate_model()
    tune.report(accuracy=accuracy)

# Define hyperparameter search space
search_space = {
    "lr": tune.grid_search([0.001, 0.01, 0.1]),
    "batch_size": tune.choice([64, 128, 256]),
    "dropout": tune.choice([0.2, 0.3, 0.5])
}

# Run Ray Tune
ray.init(address="auto")
analysis = tune.run(
    train_cifar,
    config=search_space,
    resources_per_trial={"cpu": 1},
    local_dir="./ray_results",
    verbose=1
)

# Print the best hyperparameters
print("Best hyperparameters: ", analysis.best_config)
ray.shutdown()
