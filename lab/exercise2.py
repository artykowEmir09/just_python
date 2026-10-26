import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Generate dataset (provided in the lab)
np.random.seed(10)

study_hours = np.random.uniform(1.0, 10.0, 80)
exam_scores = 35 + (study_hours * 6.5) + np.random.normal(0, 4, 80)

data_task1 = pd.DataFrame({
    'Study_Hours': study_hours,
    'Exam_Score': exam_scores
})

# 1. Feature and target selection
X = data_task1[['Study_Hours']]
y = data_task1['Exam_Score']

# 2. Train-test split (75% / 25%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=10
)

# 3. Model training
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Evaluation
y_pred = model.predict(X_test)

print("--- PRINT RESULTS ---")
print(f"Intercept: {model.intercept_:.2f}")
print(f"Coefficient: {model.coef_[0]:.2f}")

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R2 Score: {r2:.4f}")