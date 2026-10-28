# Activity 1: Simple Linear Regression
# Predicting House Prices
   
# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Generate synthetic dataset                   
np.random.seed(42)

house_size = np.random.randint(600, 3500, size=100)  # sq ft
price = house_size * 150 + np.random.normal(0, 25000, size=100)

df = pd.DataFrame({
    'Size_sqft': house_size,
    'Price': price
})

# Step 2: Separate features (X) and target (y)
X = df[['Size_sqft']]
y = df['Price']

# Step 3: Train-Test Split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 4: Model Instantiation and Fitting 
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Model Parameters
print(f"Intercept (beta_0): ${model.intercept_:.2f}")
print(f"Slope Coefficient (beta_1): ${model.coef_[0]:.2f} per sq ft")

# Step 6: Prediction and Evaluation
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Root Mean Squared Error (RMSE): ${rmse:.2f}")
print(f"R-squared Score (R2): {r2:.4f}")

# Step 7: Visualizing the Regression Line
plt.figure(figsize=(8, 5))

plt.scatter(
    X_train['Size_sqft'], y_train,
    color='blue', alpha=0.6, label='Train Data'
)

plt.scatter(
    X_test['Size_sqft'], y_test,
    color='green', alpha=0.8, label='Test Data'
)

# Sort test data to display the regression line correctly
sorted_indices = np.argsort(X_test['Size_sqft'].values)

plt.plot(
    X_test['Size_sqft'].values[sorted_indices],
    y_pred[sorted_indices],
    color='red', linewidth=2, label='Regression Line'
)

plt.xlabel('House Size (sq ft)')
plt.ylabel('Price ($)')
plt.title('Simple Linear Regression: House Size vs. Price')
plt.legend()
plt.grid(True)
plt.show()
