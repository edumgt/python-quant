# Chapter 18. LSTM — 주가 수익률 시계열 예측

> 💡 **쉽게 이해하기**: 일반 신경망은 어제 배운 내용을 잊지만, LSTM은 "기억 창고(Cell State)"와 "게이트(Gate)"로 과거 정보를 선택적으로 기억합니다. 주가처럼 순서가 중요한 시계열에서 LSTM이 강력한 이유입니다. `LSTMPredictor.py`로 직접 실습하세요.

---

## 📌 이 챕터에서 배우는 것

| 개념 | 설명 |
|------|------|
| Forget Gate | 과거 정보 중 버릴 것 선택 (sigmoid → 0: 버림, 1: 유지) |
| Input Gate | 새 정보 중 기억할 것 선택 |
| Cell State | 장기 기억 저장소 |
| Output Gate | 현재 출력할 정보 선택 |
| 방향성 정확도 | 상승/하락 방향을 맞춘 비율 (퀀트 핵심 지표) |

> **Day037 연결** — `docs/day037.md` 이론과 `src/LSTMPredictor.py` 실습을 함께 진행하세요.

---

## 🔧 실습 파일 실행

```bash
python LSTMPredictor.py
# 출력: lstm_predictor.png (손실 곡선 + 실제 vs. 예측 수익률)
```

또는 FastAPI 엔드포인트 호출:

```bash
curl -X POST http://localhost:8000/api/dl/lstm-predictor \
  -H "Content-Type: application/json" \
  -d '{"seq_len": 30, "n_days": 2000, "hidden_size": 64, "epochs": 30}'
```

---

## 🧱 모델 구조 (요약)

```
입력: (batch, 30, 1)        ← 30일 수익률 시퀀스 (피처 1개)
  │
  ▼ LSTM(hidden=64, layers=2) — 양방향 장기 의존성 학습
  ▼ 마지막 타임스텝 출력 (batch, 64)
  ▼ Linear(64→32) + ReLU
  ▼ Linear(32→1)
출력: (batch,)               ← 다음 날 수익률 예측값
```

---

## 📊 학습 결과 해석

| 지표 | 의미 |
|------|------|
| Val MSE Loss | 낮을수록 예측 오차 감소 |
| 방향성 정확도 > 0.52 | 무작위(0.50) 이상이면 통계적 유의미 |
| 과적합 | Train Loss << Val Loss → Dropout 증가, 데이터 확대 |

---

## ⚙️ 하이퍼파라미터 튜닝 팁

| 파라미터 | 권장 탐색 범위 | 영향 |
|---------|-------------|------|
| `seq_len` | 10 ~ 60 | 짧으면 최근 패턴, 길면 장기 추세 |
| `hidden_size` | 32 ~ 256 | 클수록 표현력↑, 과적합 위험↑ |
| `num_layers` | 1 ~ 3 | 깊을수록 복잡한 패턴 학습 |
| `dropout` | 0.1 ~ 0.5 | 과적합 조절 |

---

## 🔗 퀀트 연결

- **다채널 입력**: 수익률 외 RSI, 거래량, 볼린저밴드 값을 추가 피처로 사용
- **다변수 LSTM**: `input_size=N`으로 N개 팩터 동시 학습
- **Bidirectional LSTM**: 양방향 LSTM으로 더 풍부한 컨텍스트 학습 (`bidirectional=True`)

---

## 📺 참고 자료

| 주제 | 링크 |
|------|------|
| LSTM 직관적 이해 | [Understanding LSTM Networks — Colah's Blog](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) |
| PyTorch LSTM | [PyTorch 공식 문서](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html) |
