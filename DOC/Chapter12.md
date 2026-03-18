# Chapter 12. SVM Classifier — 서포트 벡터 머신 / Support Vector Machine

---

## 🇰🇷 한국어

### 핵심 개념

SVM은 클래스 경계에서 **마진(margin)**을 최대화하는 분류기입니다.  
서포트 벡터(경계에 가장 가까운 샘플)가 결정 경계를 정의합니다.

### 커널 함수

| 커널 | 특징 | 사용 상황 |
|------|------|---------|
| `linear` | 직선 경계 | 선형 분리 가능 데이터 |
| `rbf` | 가우시안 비선형 경계 | 일반적인 분류 문제 (기본값) |
| `poly` | 다항식 경계 | 곡선 패턴 |

### C 파라미터 (정규화)

- **작은 C** → 넓은 마진, 오분류 허용 (underfitting 위험)
- **큰 C** → 좁은 마진, 오분류 최소화 (overfitting 위험)

### 구현 흐름

1. 2D 분류 데이터 생성 (`make_classification`)
2. `StandardScaler` 정규화
3. `SVC(kernel=..., C=...)` 학습
4. `DecisionBoundaryDisplay`로 시각화
5. 서포트 벡터를 원으로 강조 표시

### API 확장 시 장점

- 커널과 C 값을 실시간으로 바꿔가며 결정 경계 변화 비교
- 서포트 벡터 수와 정확도를 함께 확인

---

## 🇺🇸 English

### Core Concept

SVM finds the **maximum-margin hyperplane** that best separates classes.  
Support vectors — the training samples closest to the boundary — define the decision boundary.

### Kernel Functions

| Kernel | Characteristic | When to Use |
|--------|---------------|-------------|
| `linear` | Linear boundary | Linearly separable data |
| `rbf` | Gaussian non-linear boundary | General classification (default) |
| `poly` | Polynomial boundary | Curved patterns |

### C Parameter (Regularization)

- **Small C** → wide margin, allows misclassification (risk: underfitting)
- **Large C** → narrow margin, minimizes misclassification (risk: overfitting)

### Implementation Flow

1. Generate 2D classification data (`make_classification`)
2. Normalize with `StandardScaler`
3. Fit `SVC(kernel=..., C=...)`
4. Visualize with `DecisionBoundaryDisplay`
5. Highlight support vectors with circles

### API Extension Benefits

- Change kernel and C value interactively to compare decision boundaries
- View support vector count and accuracy side-by-side
