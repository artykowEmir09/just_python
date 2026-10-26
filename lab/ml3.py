# =====================================================================
# Logistic Regression Implementation & Decision Boundary Visualization  
# =====================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1. Load Iris dataset and select the first two features for 2D plotting 
iris = load_iris()
X = iris.data[:, :2]  # Selecting Feature 1 and Feature 2
y = (iris.target != 0) * 1  # Convert target into binary classes (0 or 1)

# 2. Split dataset into 80% Training and 20% Testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Instantiate and train the Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# 4. Create a mesh grid across feature limits to plot the decision boundary
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
h = 0.02  # Step size in the mesh grid

xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Predict function values for every point across the grid surface
Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# 5. Plot the decision boundary contour and scatter the data points
plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral, alpha=0.8)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Spectral, edgecolor='k')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Logistic Regression Decision Boundary')
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()

# 6. Evaluate the model performance on test data
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))