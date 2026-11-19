# ACTIVITY 5: Convolutional Neural Networks (CNNs)

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load and normalize the dataset if it is not already loaded
digits = load_digits()
X_img = digits.data / 16.0
y_img = digits.target

X_cnn = X_img.reshape(-1, 1, 8, 8)
X_c_tr, X_c_te, y_c_tr, y_c_te = train_test_split(
    X_cnn,
    y_img,
    test_size=0.25,
    random_state=42,
    stratify=y_img
)

class MiniDigitCNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)  # 8x8 -> 4x4
        )

        self.classifier = nn.Linear(8 * 4 * 4, 10)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)  # Flatten
        return self.classifier(x)

cnn_model = MiniDigitCNN()
cnn_opt = optim.Adam(cnn_model.parameters(), lr=0.01)
cnn_crit = nn.CrossEntropyLoss()

# Training loop
train_ds_cnn = TensorDataset(
    torch.tensor(X_c_tr, dtype=torch.float32),
    torch.tensor(y_c_tr, dtype=torch.long)
)

loader_cnn = DataLoader(
    train_ds_cnn,
    batch_size=32,
    shuffle=True
)

for epoch in range(25):
    cnn_model.train()

    for bx, by in loader_cnn:
        cnn_opt.zero_grad()

        loss = cnn_crit(cnn_model(bx), by)

        loss.backward()
        cnn_opt.step()

cnn_model.eval()

with torch.no_grad():
    test_out = cnn_model(torch.tensor(X_c_te, dtype=torch.float32))
    _, test_preds = torch.max(test_out, 1)

print(
    f"Mini CNN Test Accuracy: "
    f"{accuracy_score(y_c_te, test_preds):.4f}"
)