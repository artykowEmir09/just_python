import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

# 1. Load Data & Train Model
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=42
)

scaler = StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)

# Set up side-by-side plots
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# --- PLOT 1: Confusion Matrix Heatmap ---
cm = confusion_matrix(y_test, predictions)
sns.heatmap(
    cm, annot=True, fmt='d', cmap='Blues',
    xticklabels=iris.target_names,
    yticklabels=iris.target_names,
    ax=axes[0]
)
axes[0].set_title('Confusion Matrix Heatmap', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Predicted Species', fontsize=12)
axes[0].set_ylabel('Actual Species', fontsize=12)

# --- PLOT 2: Feature Scatter Plot (Petal Length vs Petal Width) ---
test_df = pd.DataFrame(X_test, columns=iris.feature_names)
test_df['Actual Species'] = [iris.target_names[i] for i in y_test]
test_df['Predicted Species'] = [iris.target_names[i] for i in predictions]

sns.scatterplot(
    data=test_df, 
    x='petal length (cm)', 
    y='petal width (cm)', 
    hue='Predicted Species', 
    style='Actual Species',
    s=100, 
    palette='Set1',
    ax=axes[1]
)
axes[1].set_title('Petal Features vs Predicted Species', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Petal Length (cm)', fontsize=12)
axes[1].set_ylabel('Petal Width (cm)', fontsize=12)
axes[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()