from ray import tune
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def svm_train(config):
    # Load the Digits dataset
    digits = load_digits()
    X, y = digits.data, digits.target

    # Preprocess the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train the SVM with provided hyperparameters
    model = SVC(
        kernel=config["kernel"],
        C=config["C"],
        gamma=config.get("gamma", "scale"),  # gamma only for non-linear kernels
        degree=config.get("degree", 3)  # degree only for poly kernel
    )
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)

    # Report the accuracy as negative loss for Ray Tune
    tune.report(mean_loss=-accuracy)
