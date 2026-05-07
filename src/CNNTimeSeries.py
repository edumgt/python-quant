"""
CNN Time Series Classifier (1D CNN)
=====================================
Day036 대응 실습 파일 — 1D CNN으로 주가 패턴(상승·횡보·하락)을 분류합니다.
GPU 없이 CPU만으로 실행 가능합니다.

실행:
    python CNNTimeSeries.py

출력:
    - 학습/검증 손실 및 정확도 곡선 (cnn_timeseries.png)
    - 분류 리포트 (상승/횡보/하락)

퀀트 연결:
    - 과거 N일 주가 창(window)에서 "패턴 → 다음 방향" 분류
    - 실무에서는 OHLCV 다채널 입력으로 확장 가능
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ──────────────────────────────────────────────────────────────
# 1. 합성 주가 시퀀스 생성 (실무: yfinance 대체 가능)
# ──────────────────────────────────────────────────────────────
WINDOW = 20          # 입력 창 길이 (20 거래일)
N_SAMPLES = 2000
SEED = 42

rng = np.random.default_rng(SEED)

def _make_price_window(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """
    GBM(기하 브라운 운동)으로 주가 창을 생성하고
    다음 기간 수익률에 따라 레이블을 부여합니다.
      0: 하락 (< -1%)
      1: 횡보 (-1% ~ +1%)
      2: 상승 (> +1%)
    """
    rng_ = np.random.default_rng(seed)
    windows, labels = [], []
    for _ in range(n):
        mu = rng_.uniform(-0.0003, 0.0003)
        sigma = rng_.uniform(0.01, 0.025)
        returns = rng_.normal(mu, sigma, WINDOW + 1)
        prices = 100 * np.exp(np.cumsum(returns))
        win = prices[:WINDOW]
        next_ret = (prices[WINDOW] - prices[WINDOW - 1]) / prices[WINDOW - 1]
        if next_ret > 0.01:
            lbl = 2
        elif next_ret < -0.01:
            lbl = 0
        else:
            lbl = 1
        windows.append(win)
        labels.append(lbl)
    return np.array(windows, dtype=np.float32), np.array(labels, dtype=np.int64)

X_raw, y = _make_price_window(N_SAMPLES, SEED)

# 창별 Z-score 정규화
scaler = StandardScaler()
X_norm = scaler.fit_transform(X_raw).astype(np.float32)

X_train, X_test, y_train, y_test = train_test_split(
    X_norm, y, test_size=0.2, stratify=y, random_state=SEED
)

# PyTorch Dataset
X_tr = torch.tensor(X_train).unsqueeze(1)   # (N, 1, T)
X_te = torch.tensor(X_test).unsqueeze(1)
y_tr = torch.tensor(y_train)
y_te = torch.tensor(y_test)

train_ds = torch.utils.data.TensorDataset(X_tr, y_tr)
test_ds  = torch.utils.data.TensorDataset(X_te, y_te)
train_dl = torch.utils.data.DataLoader(train_ds, batch_size=64, shuffle=True)
test_dl  = torch.utils.data.DataLoader(test_ds,  batch_size=128)

# ──────────────────────────────────────────────────────────────
# 2. 1D CNN 모델 정의
# ──────────────────────────────────────────────────────────────
class CNN1D(nn.Module):
    """
    1D 합성곱 신경망 (시계열 패턴 분류)
    구조: Conv1D × 2 → GlobalAvgPool → FC × 2 → 출력(3클래스)
    """

    def __init__(self, in_channels: int = 1, num_classes: int = 3) -> None:
        super().__init__()
        self.conv_block = nn.Sequential(
            nn.Conv1d(in_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),   # Global Average Pooling
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.conv_block(x))

# ──────────────────────────────────────────────────────────────
# 3. 학습
# ──────────────────────────────────────────────────────────────
torch.manual_seed(SEED)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CNN1D().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

EPOCHS = 30
train_losses, val_losses = [], []
train_accs, val_accs = [], []

for epoch in range(EPOCHS):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for xb, yb in train_dl:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        out = model(xb)
        loss = criterion(out, yb)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(yb)
        correct += (out.argmax(1) == yb).sum().item()
        total += len(yb)
    train_losses.append(total_loss / total)
    train_accs.append(correct / total)

    model.eval()
    vloss, vcorrect, vtotal = 0.0, 0, 0
    with torch.no_grad():
        for xb, yb in test_dl:
            xb, yb = xb.to(device), yb.to(device)
            out = model(xb)
            vloss += criterion(out, yb).item() * len(yb)
            vcorrect += (out.argmax(1) == yb).sum().item()
            vtotal += len(yb)
    val_losses.append(vloss / vtotal)
    val_accs.append(vcorrect / vtotal)

    if (epoch + 1) % 5 == 0:
        print(
            f"Epoch {epoch+1:3d}/{EPOCHS}  "
            f"train_loss={train_losses[-1]:.4f}  train_acc={train_accs[-1]:.4f}  "
            f"val_loss={val_losses[-1]:.4f}  val_acc={val_accs[-1]:.4f}"
        )

# ──────────────────────────────────────────────────────────────
# 4. 평가
# ──────────────────────────────────────────────────────────────
model.eval()
all_preds = []
with torch.no_grad():
    for xb, _ in test_dl:
        all_preds.append(model(xb.to(device)).argmax(1).cpu().numpy())
y_pred = np.concatenate(all_preds)

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=["하락(0)", "횡보(1)", "상승(2)"]))

# ──────────────────────────────────────────────────────────────
# 5. 시각화
# ──────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(train_losses, label="Train Loss")
axes[0].plot(val_losses,   label="Val Loss")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Loss (Cross Entropy)")
axes[0].set_title("1D CNN — 학습/검증 손실")
axes[0].legend()
axes[0].grid(True)

axes[1].plot(train_accs, label="Train Acc")
axes[1].plot(val_accs,   label="Val Acc")
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Accuracy")
axes[1].set_title("1D CNN — 학습/검증 정확도")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("cnn_timeseries.png", dpi=140)
print("Saved cnn_timeseries.png")
