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

# Activity 1 Code: Computing Euclidean & Manhattan distances
p = np.array([2.0, 3.0])
q = np.array([5.0, 7.0])

# Euclidean distance
euclidean_dist = np.linalg.norm(p - q)
# Manhattan distance
manhattan_dist = np.sum(np.abs(p - q))

print(f"Point p: {p}, Point q: {q}")
print(f"Euclidean Distance: {euclidean_dist:.4f}")
print(f"Manhattan Distance: {manhattan_dist:.4f}")  