import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
 
np.random.seed(42)
n = 150

engine_size = np.random.uniform(1.2, 4.0, n)
age = np.random.randint(1, 15, n)
mileage = age * np.random.uniform(8, 15, n)

price = (
    35000
    + (engine_size * 4500)
    - (age * 1200)
    - (mileage * 150)
    + np.random.normal(0, 1500, n)
)

car_df = pd.DataFrame({
    'Engine_Size': engine_size,
    'Age': age,
    'Mileage': mileage,
    'Price': price
})
 
X = car_df[['Engine_Size', 'Age', 'Mileage']]
y = car_df['Price']
 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
 
model_car = LinearRegression()
model_car.fit(X_train, y_train)
 
print("--- PRINT RESULTS ---")

feature_names = X.columns

for name, coef in zip(feature_names, model_car.coef_):
    print(f"Coefficient for {name}: {coef:.2f}")

print(f"Intercept: {model_car.intercept_:.2f}")
 
train_r2 = model_car.score(X_train, y_train)
test_r2 = model_car.score(X_test, y_test)

print(f"Train R2 Score: {train_r2:.4f}")
print(f"Test R2 Score: {test_r2:.4f}")