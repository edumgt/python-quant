"""
Transformer Time Series Predictor
===================================
Day038-039 대응 실습 파일 — Transformer Encoder로 주가 시계열을 예측합니다.
GPU 없이 CPU만으로 실행 가능합니다.

실행:
    python TransformerTimeSeries.py

출력:
    - 학습/검증 손실 곡선
    - 실제 vs. 예측 주가 비교 (transformer_timeseries.png)
    - 방향성 정확도

구조:
    입력 시퀀스 → Positional Encoding → TransformerEncoder → FC Head → 다음 N스텝 예측

퀀트 연결:
    - 멀티스텝 주가 예측 (1일~5일 선물)
    - Self-Attention이 장기 의존성(계절성, 이벤트)을 포착하는 원리 이해
"""

from __future__ import annotations

import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

# ──────────────────────────────────────────────────────────────
# 1. 합성 주가 데이터 생성 (GBM + 계절성 추가)
# ──────────────────────────────────────────────────────────────
SEQ_LEN    = 40    # 인코더 입력 창 길이
PRED_STEPS = 5     # 예측할 미래 스텝 수 (5 거래일)
N_DAYS     = 2500
SEED       = 42

rng = np.random.default_rng(SEED)
t = np.arange(N_DAYS)
# GBM 수익률 + 약한 계절성 신호
trend = 0.0002 * t
seasonal = 0.02 * np.sin(2 * np.pi * t / 252)   # 연간 사이클
noise = rng.normal(0, 0.012, N_DAYS)
log_returns = 0.0001 + 0.8 * (trend / N_DAYS) + seasonal * 0.005 + noise
prices = 1000 * np.exp(np.cumsum(log_returns))

# MinMax 정규화 (0~1)
scaler = MinMaxScaler()
prices_norm = scaler.fit_transform(prices.reshape(-1, 1)).ravel().astype(np.float32)


def make_sequences(series: np.ndarray, seq_len: int, pred: int) -> tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for i in range(len(series) - seq_len - pred):
        X.append(series[i : i + seq_len])
        y.append(series[i + seq_len : i + seq_len + pred])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


X_all, y_all = make_sequences(prices_norm, SEQ_LEN, PRED_STEPS)
split = int(len(X_all) * 0.8)
X_train, X_test = X_all[:split], X_all[split:]
y_train, y_test = y_all[:split], y_all[split:]

# Tensor 변환: (N, SEQ, 1) — 피처 차원 추가
Xtr = torch.tensor(X_train).unsqueeze(-1)
Xte = torch.tensor(X_test).unsqueeze(-1)
ytr = torch.tensor(y_train)
yte = torch.tensor(y_test)

train_ds = torch.utils.data.TensorDataset(Xtr, ytr)
test_ds  = torch.utils.data.TensorDataset(Xte, yte)
train_dl = torch.utils.data.DataLoader(train_ds, batch_size=64, shuffle=True)
test_dl  = torch.utils.data.DataLoader(test_ds,  batch_size=128)

# ──────────────────────────────────────────────────────────────
# 2. 위치 인코딩 (Positional Encoding)
# ──────────────────────────────────────────────────────────────
class PositionalEncoding(nn.Module):
    """
    Vaswani et al. (2017) 위치 인코딩
    PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """

    def __init__(self, d_model: int, max_len: int = 200, dropout: float = 0.1) -> None:
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2, dtype=torch.float) * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)                  # (1, max_len, d_model)
        self.register_buffer("pe", pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.pe[:, : x.size(1), :]
        return self.dropout(x)


# ──────────────────────────────────────────────────────────────
# 3. Transformer 시계열 예측 모델
# ──────────────────────────────────────────────────────────────
class TransformerPredictor(nn.Module):
    """
    Transformer Encoder 기반 시계열 예측 모델

    구조:
      Linear(input→d_model) → PositionalEncoding
      → TransformerEncoder(N_HEADS, N_LAYERS)
      → 마지막 토큰 → Linear → PRED_STEPS 출력
    """

    def __init__(
        self,
        input_size: int = 1,
        d_model: int = 32,
        nhead: int = 4,
        num_encoder_layers: int = 2,
        dim_feedforward: int = 128,
        dropout: float = 0.1,
        pred_steps: int = PRED_STEPS,
    ) -> None:
        super().__init__()
        self.input_proj = nn.Linear(input_size, d_model)
        self.pos_enc = PositionalEncoding(d_model, dropout=dropout)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_encoder_layers)
        self.head = nn.Linear(d_model, pred_steps)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.input_proj(x)       # (B, T, d_model)
        x = self.pos_enc(x)
        x = self.encoder(x)          # (B, T, d_model)
        return self.head(x[:, -1, :])   # 마지막 토큰 → (B, pred_steps)


# ──────────────────────────────────────────────────────────────
# 4. 학습
# ──────────────────────────────────────────────────────────────
torch.manual_seed(SEED)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = TransformerPredictor().to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)
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
    scheduler.step()
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
# 5. 평가 (방향성 정확도 — 첫 번째 예측 스텝 기준)
# ──────────────────────────────────────────────────────────────
model.eval()
with torch.no_grad():
    y_pred_norm = model(Xte.to(device)).cpu().numpy()   # (N_test, PRED_STEPS)

# 역정규화
def inverse(arr: np.ndarray) -> np.ndarray:
    return scaler.inverse_transform(arr.reshape(-1, 1)).ravel()

y_pred_step1 = inverse(y_pred_norm[:, 0])
y_true_step1 = inverse(y_test[:, 0])
last_input   = inverse(X_test[:, -1])

# 방향성: 예측값이 마지막 입력보다 오를지 내릴지
dir_acc = np.mean(
    np.sign(y_pred_step1 - last_input) == np.sign(y_true_step1 - last_input)
)
print(f"\n1-step 방향성 정확도: {dir_acc:.4f}")
print(f"(참고: 무작위 기대값 ≈ 0.500)")

# ──────────────────────────────────────────────────────────────
# 6. 시각화
# ──────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 손실 곡선
axes[0].plot(train_losses, label="Train Loss")
axes[0].plot(val_losses,   label="Val Loss")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("MSE Loss")
axes[0].set_title("Transformer — 학습/검증 손실")
axes[0].legend()
axes[0].grid(True)

# 실제 vs. 예측 (마지막 120일)
plot_n = 120
axes[1].plot(y_true_step1[-plot_n:], label="실제 주가 (t+1)", alpha=0.8)
axes[1].plot(y_pred_step1[-plot_n:], label="Transformer 예측 (t+1)", alpha=0.8, linestyle="--")
axes[1].set_xlabel("거래일")
axes[1].set_ylabel("주가")
axes[1].set_title(f"Transformer 예측 vs. 실제\n방향성 정확도: {dir_acc:.2%}")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("transformer_timeseries.png", dpi=140)
print("Saved transformer_timeseries.png")
