
# ==========================================
# ACTIVITY 3: Solving the XOR Problem
# with a 2-Layer Neural Network
# ==========================================

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt


# 1. Prepare the XOR Dataset

X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])

X_xor_t = torch.tensor(
    [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]],
    dtype=torch.float32
)

y_xor_t = torch.tensor(
    [[0.0], [1.0], [1.0], [0.0]],
    dtype=torch.float32
)


# 2. Define a 2-Layer Neural Network

class XORNet(nn.Module):

    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(2, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)


# Initialize model, loss function, and optimizer

torch.manual_seed(42)

xor_model = XORNet()

criterion = nn.BCELoss()

optimizer = optim.Adam(
    xor_model.parameters(),
    lr=0.05
)


# 3. Training Loop

for epoch in range(1000):

    optimizer.zero_grad()

    predictions = xor_model(X_xor_t)

    loss = criterion(predictions, y_xor_t)

    loss.backward()

    optimizer.step()


# 4. Evaluate Predictions

xor_model.eval()

with torch.no_grad():

    probs = xor_model(X_xor_t)

    preds = (probs >= 0.5).float()

    print("--- XOR Neural Network Results ---")

    for inp, target, prob, pred in zip(
        X_xor_t, y_xor_t, probs, preds
    ):

        print(
            f"Input: {inp.numpy()} | "
            f"Actual: {int(target.item())} | "
            f"Predicted Prob: {prob.item():.4f} "
            f"-> Class {int(pred.item())}"
        )


# 5. Visualize the Non-Linear Decision Boundary

xx, yy = np.meshgrid(
    np.linspace(-0.5, 1.5, 200),
    np.linspace(-0.5, 1.5, 200)
)

grid_tensor = torch.tensor(
    np.c_[xx.ravel(), yy.ravel()],
    dtype=torch.float32
)

with torch.no_grad():

    Z = xor_model(grid_tensor).reshape(xx.shape).numpy()


plt.figure(figsize=(6, 5))

# Plot shaded decision regions

plt.contourf(
    xx, yy, Z,
    levels=[0, 0.5, 1],
    colors=['#ffcccc', '#cce5ff'],
    alpha=0.6
)

plt.contour(
    xx, yy, Z,
    levels=[0.5],
    colors='black',
    linestyles='--',
    linewidths=1.5
)


# Plot original XOR points

plt.scatter(
    X_xor[y_xor == 0, 0],
    X_xor[y_xor == 0, 1],
    color='red',
    s=120,
    label='Class 0 (Output 0)',
    marker='o',
    edgecolors='k'
)

plt.scatter(
    X_xor[y_xor == 1, 0],
    X_xor[y_xor == 1, 1],
    color='blue',
    s=120,
    label='Class 1 (Output 1)',
    marker='s',
    edgecolors='k'
)


plt.title(
    'XOR Solved! Non-Linear Decision Boundary with 1 Hidden Layer'
)

plt.xlabel('Input X1')
plt.ylabel('Input X2')

plt.xlim(-0.5, 1.5)
plt.ylim(-0.5, 1.5)

plt.grid(True, linestyle=':', alpha=0.6)

plt.legend()

plt.show()
