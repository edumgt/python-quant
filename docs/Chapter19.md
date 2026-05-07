# Chapter 19. Transformer — 시계열 주가 멀티스텝 예측

> 💡 **쉽게 이해하기**: LSTM이 "앞에서 뒤로 차례로 읽는 독자"라면, Transformer는 "모든 단어를 동시에 보고 중요한 곳에 집중(Attention)하는 독자"입니다. 더 긴 의존성을 병렬로 학습해 최신 AI(GPT, BERT)의 기반이 됩니다. `TransformerTimeSeries.py`로 직접 실습하세요.

---

## 📌 이 챕터에서 배우는 것

| 개념 | 설명 |
|------|------|
| Self-Attention | 시퀀스 내 모든 타임스텝 쌍의 관계를 학습 |
| Multi-Head Attention | 여러 관점(헤드)에서 패턴을 동시에 탐색 |
| Positional Encoding | 순서 정보 주입 (sin/cos 함수) |
| TransformerEncoder | 인코더만 사용한 판별·예측 모델 |
| 멀티스텝 예측 | 1일이 아닌 5일 앞까지 동시에 예측 |

> **Day038-039 연결** — `docs/day038.md`(Transformer 기초), `docs/day039.md`(시계열 전용 모델) 이론과 `src/TransformerTimeSeries.py` 실습을 함께 진행하세요.

---

## 🔧 실습 파일 실행

```bash
python TransformerTimeSeries.py
# 출력: transformer_timeseries.png (손실 곡선 + 실제 vs. 예측 주가)
```

또는 FastAPI 엔드포인트 호출:

```bash
curl -X POST http://localhost:8000/api/dl/transformer-timeseries \
  -H "Content-Type: application/json" \
  -d '{"seq_len": 40, "pred_steps": 5, "d_model": 32, "epochs": 30}'
```

---

## 🧱 모델 구조 (요약)

```
입력: (batch, 40, 1)            ← 40일 정규화 주가 시퀀스
  │
  ▼ Linear(1 → d_model=32)      ← 피처 차원 확장
  ▼ Positional Encoding          ← 순서 정보 주입
  ▼ TransformerEncoder
  │    └─ EncoderLayer × 2
  │         ├─ Multi-Head Self-Attention (nhead=4)
  │         └─ Feed-Forward(128) + LayerNorm + Dropout
  ▼ 마지막 토큰 (batch, d_model)
  ▼ Linear(d_model → pred_steps=5)
출력: (batch, 5)                 ← 미래 5 거래일 예측값
```

---

## 📊 Self-Attention 직관 (주가 시계열)

```
오늘 주가가 급등했을 때, 모델이 주목하는 과거 타임스텝:
  t-252일 (1년 전 같은 시기)  ← 계절성 패턴 포착
  t-5일 (직전 주)              ← 단기 추세 포착
  t-20일 (직전 달)             ← 중기 사이클 포착
→ 각 타임스텝에 중요도(Attention Weight) 부여 후 가중 합산
```

---

## ⚙️ 하이퍼파라미터 가이드

| 파라미터 | 설명 | 권장값 |
|---------|------|-------|
| `seq_len` | 인코더 입력 길이 | 20~80 거래일 |
| `pred_steps` | 예측 스텝 수 | 1~10일 |
| `d_model` | 임베딩 차원 | 32~128 (nhead의 배수) |
| `nhead` | Attention 헤드 수 | d_model / 8 권장 |
| `num_encoder_layers` | 인코더 레이어 수 | 2~4 |

---

## 🔗 최신 시계열 Transformer 모델 (심화)

| 모델 | 특징 | 논문 |
|------|------|------|
| **Informer** | 희소 Attention(ProbSparse), 장기 예측 | Zhou et al., 2021 |
| **PatchTST** | 패치 단위 분할로 지역 의미 보존 | Nie et al., 2023 |
| **TimesNet** | 2D 변환으로 시간 변동 모델링 | Wu et al., 2023 |
| **iTransformer** | 변수(채널) 축으로 Attention 적용 | Liu et al., 2024 |

---

## 🔗 퀀트 연결

- **포트폴리오 적용**: 여러 종목의 미래 5일 수익률을 동시 예측 → 비중 조절
- **어텐션 맵 시각화**: 어느 과거 날짜에 집중하는지 분석 → 계절성·이벤트 확인
- **앙상블**: Transformer + LSTM + CNN 예측값 평균 → 더 안정적인 신호

---

## 📺 참고 자료

| 주제 | 링크 |
|------|------|
| Attention Is All You Need | [논문 원문 (arXiv)](https://arxiv.org/abs/1706.03762) |
| Transformer 시각적 설명 | [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/) |
| PyTorch TransformerEncoder | [PyTorch 공식 문서](https://pytorch.org/docs/stable/generated/torch.nn.TransformerEncoder.html) |
