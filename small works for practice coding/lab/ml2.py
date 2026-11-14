# =====================================================================
# Visualizing Decision Boundaries with Scikit-learn & Matplotlib
# =====================================================================

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import DecisionBoundaryDisplay

# 1. Load Iris dataset and select 2 features for 2D plotting
# Column 2: Petal Length (cm)
# Column 3: Petal Width (cm)

iris = load_iris()

X_2d = iris.data[:, 2:4]
y = iris.target

# 2. Instantiate and train Logistic Regression model
clf = LogisticRegression(random_state=42)
clf.fit(X_2d, y)

# 3. Create the 2D Decision Boundary Plot
fig, ax = plt.subplots(figsize=(9, 6))

# Plot decision regions
DecisionBoundaryDisplay.from_estimator(
    clf,
    X_2d,
    response_method="predict",
    cmap=plt.cm.Spectral,
    alpha=0.6,
    ax=ax,
    xlabel=iris.feature_names[2],
    ylabel=iris.feature_names[3]
)

# Overlay the actual data points
scatter = ax.scatter(
    X_2d[:, 0],
    X_2d[:, 1],
    c=y,
    cmap=plt.cm.Spectral,
    edgecolors="k",
    s=70
)

# Add custom legend matching species names
handles, _ = scatter.legend_elements()

ax.legend(
    handles,
    iris.target_names,
    loc="upper left",
    title="Species"
)

ax.set_title(
    "Logistic Regression Decision Boundaries\n"
    "(Petal Length vs. Petal Width)",
    fontsize=14,
    fontweight="bold"
)

ax.grid(True, linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()