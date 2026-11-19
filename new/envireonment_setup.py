# ENVIRONMENT SETUP FOR GOOGLE COLAB
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Set random seeds for reproducibility
np.random.seed(42)
torch.manual_seed(42)
print('✅ Environment & PyTorch configured successfully!')