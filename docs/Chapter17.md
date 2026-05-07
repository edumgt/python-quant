# Chapter 17. 1D CNN — 시계열 주가 패턴 분류

> 💡 **쉽게 이해하기**: 주가 차트 20일치를 보고 "다음 날 오를까, 내릴까, 옆으로 갈까?"를 판단하는 것은 패턴 인식입니다. 1D CNN은 이미지에서 가장자리를 찾듯, 시계열에서 상승·하락 패턴을 자동으로 학습합니다. `CNNTimeSeries.py`로 직접 확인해 보세요.

---

## 📌 이 챕터에서 배우는 것

| 개념 | 설명 |
|------|------|
| 1D 합성곱(Conv1d) | 시간축 방향으로 슬라이딩하며 패턴 추출 |
| 풀링(Pooling) | 특징 압축 — Global Average Pooling으로 고정 크기 출력 |
| 분류 헤드 | FC → Softmax(3클래스: 상승/횡보/하락) |
| 과적합 방지 | Dropout, 교차 검증 |

> **Day036 연결** — `docs/day036.md` 이론과 `src/CNNTimeSeries.py` 실습을 함께 진행하세요.

---

## 🔧 실습 파일 실행

```bash
python CNNTimeSeries.py
# 출력: cnn_timeseries.png (학습 손실·정확도 곡선)
```

또는 FastAPI 엔드포인트 호출:

```bash
curl -X POST http://localhost:8000/api/dl/cnn-timeseries \
  -H "Content-Type: application/json" \
  -d '{"window": 20, "n_samples": 2000, "epochs": 20}'
```

---

## 🧱 모델 구조 (요약)

```
입력: (batch, 1, 20)     ← 20일 주가 창 (채널 1개)
  │
  ▼ Conv1d(1→32, kernel=3) + ReLU
  ▼ Conv1d(32→64, kernel=3) + ReLU
  ▼ AdaptiveAvgPool1d(1)   ← Global Average Pooling
  ▼ Flatten → Linear(64→32) + ReLU + Dropout(0.3)
  ▼ Linear(32→3)
출력: (batch, 3)          ← [하락, 횡보, 상승] 확률
```

---

## 📊 학습 결과 해석

| 지표 | 의미 |
|------|------|
| Train Loss↓ / Val Loss↓ | 정상 학습 |
| Val Acc > 0.38 | 3-클래스 랜덤 기대값(0.33)을 상회하면 패턴 학습 중 |
| Val Acc >> Train Acc | 데이터 부족 또는 모델 구조 검토 필요 |

---

## 🔗 퀀트 연결

- **실무 확장**: OHLCV 5채널 입력(`Conv1d(in_channels=5, ...)`)으로 더 풍부한 패턴 학습 가능
- **백테스팅**: 상승 신호 → 매수, 하락 신호 → 숏/현금 보유 전략으로 연결
- **앙상블**: CNN 신호 + RSI/MACD 결합으로 False Positive 감소

---

## 📺 참고 자료

| 주제 | 링크 |
|------|------|
| 1D CNN 시계열 | [Keras: Timeseries classification from scratch](https://keras.io/examples/timeseries/timeseries_classification_from_scratch/) |
| PyTorch Conv1d | [PyTorch 공식 문서](https://pytorch.org/docs/stable/generated/torch.nn.Conv1d.html) |
