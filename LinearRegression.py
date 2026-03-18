"""
Linear & Polynomial Regression Example
=======================================
Covers simple linear regression and polynomial regression for non-linear data.
Run standalone:
    python LinearRegression.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

# ------------------------------------------------------------------
# 1. Synthetic data
# ------------------------------------------------------------------
rng = np.random.default_rng(42)
X = rng.uniform(0, 10, size=(200, 1))
y_linear = 3.5 * X.ravel() + 7 + rng.normal(0, 2, 200)
y_poly = 0.5 * X.ravel() ** 2 - 4 * X.ravel() + 10 + rng.normal(0, 3, 200)

# ------------------------------------------------------------------
# 2a. Simple linear regression
# ------------------------------------------------------------------
lin_model = LinearRegression()
lin_model.fit(X, y_linear)
y_lin_pred = lin_model.predict(X)
lin_r2 = r2_score(y_linear, y_lin_pred)
lin_mse = mean_squared_error(y_linear, y_lin_pred)
print(f"[Linear]  R²={lin_r2:.4f}  MSE={lin_mse:.4f}")
print(f"          coef={lin_model.coef_[0]:.3f}  intercept={lin_model.intercept_:.3f}")

# ------------------------------------------------------------------
# 2b. Polynomial regression
# ------------------------------------------------------------------
poly_model = make_pipeline(PolynomialFeatures(degree=2, include_bias=False), LinearRegression())
poly_model.fit(X, y_poly)
X_plot = np.linspace(0, 10, 200).reshape(-1, 1)
y_poly_pred = poly_model.predict(X_plot)
poly_r2 = r2_score(y_poly, poly_model.predict(X))
print(f"[Poly d=2] R²={poly_r2:.4f}  MSE={mean_squared_error(y_poly, poly_model.predict(X)):.4f}")

# ------------------------------------------------------------------
# 3. Visualize
# ------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Linear plot
axes[0].scatter(X, y_linear, alpha=0.5, s=15, label="Data")
axes[0].plot(np.sort(X, axis=0), lin_model.predict(np.sort(X, axis=0)), "r-", linewidth=2, label="Fit")
axes[0].set_title(f"Linear Regression  R²={lin_r2:.3f}")
axes[0].set_xlabel("X")
axes[0].set_ylabel("y")
axes[0].legend()
axes[0].grid(True)

# Polynomial plot
axes[1].scatter(X, y_poly, alpha=0.5, s=15, label="Data")
axes[1].plot(X_plot, y_poly_pred, "r-", linewidth=2, label="Poly (degree=2)")
axes[1].set_title(f"Polynomial Regression  R²={poly_r2:.3f}")
axes[1].set_xlabel("X")
axes[1].set_ylabel("y")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("regression_result.png", dpi=140)
print("Saved regression_result.png")
