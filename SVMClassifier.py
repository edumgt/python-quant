"""
SVM Classifier Example
======================
Demonstrates a Support Vector Machine classifier with an RBF kernel.
Visualizes the decision boundary and support vectors.
Run standalone:
    python SVMClassifier.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# ------------------------------------------------------------------
# 1. Data
# ------------------------------------------------------------------
X, y = make_classification(
    n_samples=300,
    n_features=2,
    n_redundant=0,
    n_informative=2,
    n_clusters_per_class=1,
    random_state=42,
)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# ------------------------------------------------------------------
# 2. Train SVM
# ------------------------------------------------------------------
svm = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42)
svm.fit(X_train, y_train)
y_pred = svm.predict(X_test)

print(classification_report(y_test, y_pred))

# ------------------------------------------------------------------
# 3. Visualize
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
DecisionBoundaryDisplay.from_estimator(
    svm, X_scaled, ax=ax, alpha=0.3, cmap=plt.cm.coolwarm, response_method="predict"
)
ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=plt.cm.coolwarm, edgecolors="k", label="Train")
ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=plt.cm.coolwarm, marker="^", edgecolors="k", label="Test")

# Mark support vectors
ax.scatter(
    svm.support_vectors_[:, 0],
    svm.support_vectors_[:, 1],
    s=100,
    linewidth=1.5,
    facecolors="none",
    edgecolors="k",
    label="Support Vectors",
)
ax.set_title("SVM (RBF Kernel) Decision Boundary")
ax.legend(loc="upper right")
ax.grid(True)
plt.tight_layout()
plt.savefig("svm_result.png", dpi=140)
print("Saved svm_result.png")
