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
# Generate a noisy synthetic dataset
X_syn, y_syn = make_classification(
    n_samples=500,
    n_features=10,
    n_informative=5,
    n_redundant=2,
    flip_y=0.1,
    random_state=42
)

X_syn_tr, X_syn_te, y_syn_tr, y_syn_te = train_test_split(
    X_syn, y_syn, test_size=0.25, random_state=42
)

# Train Single Tree vs. Random Forest (100 trees)
dt = DecisionTreeClassifier(random_state=42)
rf = RandomForestClassifier(
    n_estimators=100,
    max_features="sqrt",
    random_state=42
)

dt.fit(X_syn_tr, y_syn_tr)
rf.fit(X_syn_tr, y_syn_tr)

print(
    f"Decision Tree -> Test Accuracy: "
    f"{dt.score(X_syn_te, y_syn_te):.4f}"
)
print(
    f"Random Forest (100 trees) -> Test Accuracy: "
    f"{rf.score(X_syn_te, y_syn_te):.4f}"
)

# Plot Feature Importances from Random Forest
plt.figure(figsize=(8, 4))

feat_importances = pd.Series(
    rf.feature_importances_,
    index=[f"Feat {i}" for i in range(10)]
)

feat_importances.sort_values().plot(kind="barh", color="#2F5496")
plt.title("Random Forest Feature Importances")
plt.xlabel("MDI Feature Importance Score")
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()