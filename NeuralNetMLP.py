"""
Neural Network (MLP) Classifier Example
========================================
Uses scikit-learn's MLPClassifier to train a small feedforward neural network.
No GPU required — runs on CPU for educational clarity.
Run standalone:
    python NeuralNetMLP.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

# ------------------------------------------------------------------
# 1. Data
# ------------------------------------------------------------------
X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_informative=6,
    n_redundant=2,
    n_classes=2,
    random_state=42,
)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ------------------------------------------------------------------
# 2. Train MLP
# ------------------------------------------------------------------
mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),
    activation="relu",
    solver="adam",
    max_iter=300,
    random_state=42,
)
mlp.fit(X_train, y_train)
y_pred = mlp.predict(X_test)

print("=== Classification Report ===")
print(classification_report(y_test, y_pred))
print(f"Training iterations: {mlp.n_iter_}")

# ------------------------------------------------------------------
# 3. Visualize loss curve
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(mlp.loss_curve_, linewidth=2)
ax.set_xlabel("Iteration")
ax.set_ylabel("Loss")
ax.set_title("MLP Training Loss Curve")
ax.grid(True)
plt.tight_layout()
plt.savefig("mlp_loss.png", dpi=140)
print("Saved mlp_loss.png")
