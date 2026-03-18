# Chapter 13. MLP Neural Network — 다층 퍼셉트론 신경망 / Multi-Layer Perceptron

---

## 🇰🇷 한국어

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

## 🇺🇸 English

### Core Concept

An MLP (Multi-Layer Perceptron) is the most fundamental feedforward neural network:

```
Input features → [128] → [64] → [32] → Output class
                  ReLU    ReLU   ReLU
```

### Backpropagation

- Compute prediction error (loss) → propagate gradient backward → update weights
- `Adam` optimizer: automatically adjusts learning rate for fast convergence

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `hidden_layer_sizes` | Neurons per hidden layer e.g. `(128, 64, 32)` |
| `activation` | Activation function (`relu`, `tanh`, `logistic`) |
| `solver` | Optimizer (`adam`, `sgd`) |
| `max_iter` | Maximum epochs |

### Reading the Loss Curve

- **Monotonically decreasing** → normal training
- **Sharp drop then plateau** → converged
- **Oscillations** → learning rate too high (or insufficient data)

### Sklearn MLP vs PyTorch/TensorFlow

| Aspect | sklearn MLP | PyTorch/TF |
|--------|------------|------------|
| Difficulty | Easy | Medium–Hard |
| GPU support | ❌ | ✅ |
| Flexibility | Limited | Very high |
| Educational use | ✅ Concept learning | ✅ Production learning |
