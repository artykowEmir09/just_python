import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# 1. Load California Housing data from Colab sample files
train_path = "/content/sample_data/california_housing_train.csv"
test_path = "/content/sample_data/california_housing_test.csv"

if os.path.exists(train_path) and os.path.exists(test_path):
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)
    df = pd.concat([df_train, df_test], ignore_index=True)

    df = df.rename(columns={
        "median_house_value": "MedHouseVal",
        "median_income": "MedInc",
        "total_rooms": "AveRooms"  
    })           

    # Express house values in units of $100,000
    df["MedHouseVal"] = df["MedHouseVal"] / 100000.0

    # Calculate average rooms per household           
    df["AveRooms"] = df["AveRooms"] / df["households"]
else:
    raise FileNotFoundError(        
        "Colab sample data not found. Please verify /content/sample_data/."
    )

print("Dataset shape:", df.shape)                 
print("\nFirst 5 rows:")
print(df.head())

# 2. Select features and target
X = df[["MedInc", "AveRooms"]]
y = df["MedHouseVal"]

# 3. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# 4. Create KNN regressor
knn_model = make_pipeline(
    StandardScaler(),
    KNeighborsRegressor(n_neighbors=10)
)

# 5. Create Random Forest regressor
rf_model = RandomForestRegressor(
    n_estimators=50,
    random_state=42
)

# 6. Train both models
knn_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

# 7. Make predictions
knn_predictions = knn_model.predict(X_test)
rf_predictions = rf_model.predict(X_test)

# 8. Calculate evaluation metrics
knn_mse = mean_squared_error(y_test, knn_predictions)
knn_r2 = r2_score(y_test, knn_predictions)

rf_mse = mean_squared_error(y_test, rf_predictions)
rf_r2 = r2_score(y_test, rf_predictions)

# 9. Display results
print("\nMODEL PERFORMANCE COMPARISON")

print("\nK-Nearest Neighbors Regression")
print(f"Test MSE: {knn_mse:.4f}")
print(f"Test R²:  {knn_r2:.4f}")

print("\nRandom Forest Regression")
print(f"Test MSE: {rf_mse:.4f}")
print(f"Test R²:  {rf_r2:.4f}")