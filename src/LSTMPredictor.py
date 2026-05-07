"""
LSTM Stock Price Predictor
==========================
Day037 대응 실습 파일 — LSTM으로 다음 날 주가 수익률(방향)을 예측합니다.
GPU 없이 CPU만으로 실행 가능합니다.

실행:
    python LSTMPredictor.py

출력:
    - 학습/검증 손실 곡선
    - 실제 vs. 예측 수익률 비교 (lstm_predictor.png)
    - 분류 정확도 (상승/하락 방향 맞춤률)

퀀트 연결:
    - 과거 SEQ_LEN일 수익률 시퀀스 → 다음 날 수익률 예측
    - 실무에서는 다양한 팩터(RSI, 거래량 등)를 채널로 추가 가능
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler

# ──────────────────────────────────────────────────────────────
# 1. 합성 주가 데이터 생성 (GBM)
# ──────────────────────────────────────────────────────────────
SEQ_LEN = 30          # 입력 시퀀스 길이 (30 거래일)
N_DAYS  = 2000        # 전체 시뮬레이션 일수
SEED    = 42

rng = np.random.default_rng(SEED)
mu, sigma = 0.0002, 0.015
daily_ret = rng.normal(mu, sigma, N_DAYS)
prices = 1000 * np.exp(np.cumsum(daily_ret))

# 슬라이딩 윈도우로 (X, y) 구성
def make_sequences(series: np.ndarray, seq_len: int) -> tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for i in range(len(series) - seq_len):
        X.append(series[i : i + seq_len])
        y.append(series[i + seq_len])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

returns = np.diff(prices) / prices[:-1]     # 일별 수익률
X_raw, y_raw = make_sequences(returns, SEQ_LEN)

# 정규화
scaler_X = StandardScaler()
scaler_y = StandardScaler()
X_norm = scaler_X.fit_transform(X_raw).astype(np.float32)
y_norm = scaler_y.fit_transform(y_raw.reshape(-1, 1)).ravel().astype(np.float32)

# Train / Test split (시계열 순서 유지 — 무작위 섞지 않음)
# 슬라이딩 윈도우 단위의 DataLoader 셔플은 훈련 일반화에 도움이 됩니다.
split = int(len(X_norm) * 0.8)
X_train, X_test = X_norm[:split], X_norm[split:]
y_train, y_test = y_norm[:split], y_norm[split:]
y_test_raw = y_raw[split:]   # 역정규화용 실제 수익률

# PyTorch Tensor: LSTM 입력 형태 = (batch, seq_len, input_size)
Xtr = torch.tensor(X_train).unsqueeze(-1)   # (N, SEQ, 1)
Xte = torch.tensor(X_test).unsqueeze(-1)
ytr = torch.tensor(y_train)
yte = torch.tensor(y_test)

train_ds = torch.utils.data.TensorDataset(Xtr, ytr)
test_ds  = torch.utils.data.TensorDataset(Xte, yte)
train_dl = torch.utils.data.DataLoader(train_ds, batch_size=64, shuffle=True)
test_dl  = torch.utils.data.DataLoader(test_ds,  batch_size=128)

# ──────────────────────────────────────────────────────────────
# 2. LSTM 모델 정의
# ──────────────────────────────────────────────────────────────
class LSTMRegressor(nn.Module):
    """
    2-layer LSTM → 선형 출력 (다음 날 수익률 회귀)

    Args:
        input_size:  입력 피처 수 (수익률 1개 → 1)
        hidden_size: LSTM 은닉 유닛 수
        num_layers:  LSTM 스택 수
        dropout:     레이어 간 드롭아웃 (num_layers > 1 시 적용)
    """

    def __init__(
        self,
        input_size: int = 1,
        hidden_size: int = 64,
        num_layers: int = 2,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.lstm(x)          # (batch, seq, hidden)
        last = out[:, -1, :]           # 마지막 타임스텝만 사용
        return self.fc(last).squeeze(-1)

# ──────────────────────────────────────────────────────────────
# 3. 학습
# ──────────────────────────────────────────────────────────────
torch.manual_seed(SEED)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = LSTMRegressor().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
criterion = nn.MSELoss()

EPOCHS = 50
train_losses, val_losses = [], []

for epoch in range(EPOCHS):
    model.train()
    tloss, n = 0.0, 0
    for xb, yb in train_dl:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()
        pred = model(xb)
        loss = criterion(pred, yb)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        tloss += loss.item() * len(yb)
        n += len(yb)
    train_losses.append(tloss / n)

    model.eval()
    vloss, vn = 0.0, 0
    with torch.no_grad():
        for xb, yb in test_dl:
            xb, yb = xb.to(device), yb.to(device)
            vloss += criterion(model(xb), yb).item() * len(yb)
            vn += len(yb)
    val_losses.append(vloss / vn)

    if (epoch + 1) % 10 == 0:
        print(
            f"Epoch {epoch+1:3d}/{EPOCHS}  "
            f"train_loss={train_losses[-1]:.6f}  val_loss={val_losses[-1]:.6f}"
        )

# ──────────────────────────────────────────────────────────────
# 4. 평가 — 방향성 정확도 (상승/하락 맞춤률)
# ──────────────────────────────────────────────────────────────
model.eval()
with torch.no_grad():
    y_pred_norm = model(Xte.to(device)).cpu().numpy()

# 역정규화
y_pred_raw = scaler_y.inverse_transform(y_pred_norm.reshape(-1, 1)).ravel()
direction_acc = np.mean(np.sign(y_pred_raw) == np.sign(y_test_raw))
print(f"\n방향성 정확도 (상승/하락): {direction_acc:.4f}")
print(f"(참고: 무작위 기대값 ≈ 0.500)")

# ──────────────────────────────────────────────────────────────
# 5. 시각화
# ──────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 손실 곡선
axes[0].plot(train_losses, label="Train Loss")
axes[0].plot(val_losses,   label="Val Loss")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("MSE Loss")
axes[0].set_title("LSTM — 학습/검증 손실")
axes[0].legend()
axes[0].grid(True)

# 실제 vs. 예측 수익률 (마지막 100일)
plot_n = 100
axes[1].plot(y_test_raw[-plot_n:] * 100, label="실제 수익률 (%)", alpha=0.7)
axes[1].plot(y_pred_raw[-plot_n:] * 100, label="LSTM 예측 (%)", alpha=0.7, linestyle="--")
axes[1].axhline(0, color="gray", linewidth=0.8)
axes[1].set_xlabel("거래일")
axes[1].set_ylabel("일별 수익률 (%)")
axes[1].set_title(f"LSTM 예측 vs. 실제 (방향성 정확도: {direction_acc:.2%})")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("lstm_predictor.png", dpi=140)
print("Saved lstm_predictor.png")
