import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import (
    load_iris, fetch_california_housing, make_classification
)
from sklearn.model_selection import (
    train_test_split, cross_val_score, KFold
)
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import (
    DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
)
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor
)
from sklearn.metrics import (
    accuracy_score, classification_report,
    mean_squared_error, r2_score, confusion_matrix
)

np.random.seed(42)

print("✅ All dependencies successfully loaded!")
# Load Iris dataset for 3-class classification
iris = load_iris()
X, y = iris.data, iris.target

# Split into 80% train and 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Evaluate k from 1 to 25 using 5-Fold Cross-Validation
k_values = range(1, 26)
cv_scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(
        knn, X_train_scaled, y_train, cv=5, scoring="accuracy"
    )
    cv_scores.append(scores.mean())

# Find best k
best_k = k_values[np.argmax(cv_scores)]
print(
    f"Best k found via 5-Fold CV: k = {best_k} "
    f"with accuracy {max(cv_scores):.4f}"
)

# Plot Cross-Validation Accuracy vs. k
plt.figure(figsize=(8, 4))
plt.plot(k_values, cv_scores, marker="o", color="#1F4E79", linewidth=2)
plt.title("k-NN 5-Fold Cross-Validation Accuracy vs. k")
plt.xlabel("Number of Neighbors (k)")
plt.ylabel("Mean CV Accuracy")
plt.grid(True, linestyle="--", alpha=0.6)
plt.axvline(
    best_k, color="red", linestyle=":", label=f"Optimal k = {best_k}"
)
plt.legend()
plt.show()