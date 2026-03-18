"""
KMeans Clustering Example
=========================
Demonstrates unsupervised clustering with KMeans on a 2D dataset.
Run standalone:
    python KMeansClustering.py
"""

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# ------------------------------------------------------------------
# 1. Generate sample data
# ------------------------------------------------------------------
X, y_true = make_blobs(n_samples=400, centers=4, cluster_std=0.8, random_state=42)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ------------------------------------------------------------------
# 2. Fit KMeans
# ------------------------------------------------------------------
k = 4
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)
centers = kmeans.cluster_centers_

sil = silhouette_score(X_scaled, labels)
inertia = kmeans.inertia_

print(f"K={k}  Silhouette Score: {sil:.4f}   Inertia: {inertia:.2f}")

# ------------------------------------------------------------------
# 3. Elbow Method (optional exploration)
# ------------------------------------------------------------------
inertias = []
ks = range(2, 9)
for ki in ks:
    km = KMeans(n_clusters=ki, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

# ------------------------------------------------------------------
# 4. Visualize
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap="tab10", alpha=0.7, s=20)
axes[0].scatter(centers[:, 0], centers[:, 1], c="red", marker="X", s=200, zorder=5, label="Centroids")
axes[0].set_title(f"KMeans Clustering (k={k})\nSilhouette={sil:.3f}")
axes[0].legend()
axes[0].grid(True)

axes[1].plot(list(ks), inertias, "bo-")
axes[1].set_xlabel("Number of Clusters (k)")
axes[1].set_ylabel("Inertia")
axes[1].set_title("Elbow Method")
axes[1].grid(True)

plt.tight_layout()
plt.savefig("kmeans_result.png", dpi=140)
print("Saved kmeans_result.png")
