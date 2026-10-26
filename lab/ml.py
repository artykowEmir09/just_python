# =====================================================================
# Section 4: Basics of Machine Learning with Scikit-learn
# Complete Workflow: Load -> Split -> Preprocess -> Train -> Evaluate
# =====================================================================

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, mean_squared_error

# 1. DATA PREPARATION: Load the built-in Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# 2. DATA PREPARATION: Split into Training (70%) and Testing (30%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 3. DATA PREPROCESSING: Fit StandardScaler on train data and transform test data
scaler = StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. BUILDING & TRAINING MODEL: Instantiate and fit Logistic Regression model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# 5. PREDICTION: Generate predictions on the scaled test set
predictions = model.predict(X_test_scaled)

# 6. MODEL EVALUATION: Calculate Accuracy and Mean Squared Error (MSE)
accuracy = accuracy_score(y_test, predictions)
mse = mean_squared_error(y_test, predictions)

# Print final results
print("================ MODEL RESULTS ================")
print(f"Accuracy Score: {accuracy:.2f} ({accuracy * 100:.1f}%)")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print("===============================================")