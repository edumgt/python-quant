# Chapter 03. Decision Boundary 시각화 해설 / Decision Boundary Visualization

---

## 🇰🇷 한국어

`DecisionBoundary.py`는 모델이 공간을 어떻게 나누는지 시각적으로 보여줍니다.

### 핵심 개념
- 입력 특징이 2차원일 때, 모델은 평면 위의 경계를 학습
- 경계 한쪽은 클래스 0, 다른 쪽은 클래스 1로 예측

### 구현 흐름
1. 2차원 데이터 생성
2. 학습/검증 분리
3. 로지스틱 회귀 학습
4. `meshgrid`로 촘촘한 점 생성
5. 각 점 예측 결과를 색으로 렌더링

### API/클라우드 관점
- 서버에서 PNG를 생성해 base64로 전달
- 브라우저는 `<img>`로 즉시 표시
- 원격 환경에서도 `plt.show()` 없이 동일한 시각화 제공

---

## 🇺🇸 English

`DecisionBoundary.py` visually shows how a model partitions the feature space.

### Core Concept
- With 2D input features, the model learns a boundary on a plane
- One side predicts class 0, the other predicts class 1

### Implementation Flow
1. Generate 2D data
2. Train/test split
3. Train Logistic Regression
4. Create a dense grid with `meshgrid`
5. Color each grid point by predicted class

### API/Cloud Perspective
- Server generates PNG and returns it as base64
- Browser renders instantly with an `<img>` tag
- Works in headless server environments without `plt.show()`

