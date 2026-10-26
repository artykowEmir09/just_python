import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("All libraries imported successfully!")

# What each library does:
# - NumPy: numerical calculations and random data.
# - Pandas: creates and manages datasets using DataFrames.
# - Matplotlib and Seaborn: data visualization.
# - train_test_split: divides data into training and testing sets.
# - LinearRegression: creates the regression model.
# - mean_squared_error, mean_absolute_error, and r2_score: evaluate model predictions.