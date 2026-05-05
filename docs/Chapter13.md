# Chapter 13. MLP Neural Network — 다층 퍼셉트론 신경망

> 💡 **쉽게 이해하기**: 사람의 뇌처럼 뉴런이 여러 층으로 연결된 신경망입니다. 입력이 들어오면 층을 거치며 변환되고, 틀린 예측만큼 오차를 역방향으로 전파(역전파)하여 가중치를 조금씩 수정하며 학습합니다.

---

### 핵심 개념

MLP(Multi-Layer Perceptron)는 **입력층 → 은닉층(들) → 출력층**으로 구성된 가장 기본적인 피드포워드 신경망입니다.

```
입력 특성 → [128] → [64] → [32] → 출력 클래스
               ReLU    ReLU   ReLU
```

### 역전파(Backpropagation)

- 예측 오차(손실)를 계산 → 그래디언트 역전파 → 가중치 업데이트
- `Adam` 옵티마이저: 학습률을 자동 조절하여 빠른 수렴

### 주요 파라미터

| 파라미터 | 설명 |
|--------|------|
| `hidden_layer_sizes` | 각 은닉층 뉴런 수 예: `(128, 64, 32)` |
| `activation` | 활성화 함수 (`relu`, `tanh`, `logistic`) |
| `solver` | 옵티마이저 (`adam`, `sgd`) |
| `max_iter` | 최대 에포크 수 |

### 손실 곡선 해석

- 손실이 **단조 감소** → 정상 학습
- **급격한 하락 후 정체** → 학습 완료 또는 수렴
- **진동** → 학습률이 너무 큼 (또는 소량 데이터)

### Scikit-learn MLP vs PyTorch/TensorFlow

| 항목 | sklearn MLP | PyTorch/TF |
|------|------------|------------|
| 난이도 | 쉬움 | 중간~어려움 |
| GPU 지원 | ❌ | ✅ |
| 유연성 | 제한적 | 매우 높음 |
| 교육 용도 | ✅ 개념 학습 | ✅ 실무 학습 |

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| 신경망 기초 (MLP 개념) | 3Blue1Brown | [But what is a neural network?](https://www.youtube.com/watch?v=aircAruvnKk) |
| 역전파 (Backpropagation) | 3Blue1Brown | [Backpropagation, Clearly Explained](https://www.youtube.com/watch?v=Ilg3gGewQ5U) |
| Adam 옵티마이저 | StatQuest | [Adam Optimizer, Clearly Explained!!!](https://www.youtube.com/watch?v=JXQT_vxqwIs) |
| PyTorch 입문 | freeCodeCamp | [PyTorch for Deep Learning - Full Course](https://www.youtube.com/watch?v=V_xro1bcAuA) |
