# Chapter 12. SVM Classifier — 서포트 벡터 머신

> 💡 **쉽게 이해하기**: 두 그룹 사이에 경계선을 긋되, 양쪽 그룹과 가장 멀리 떨어진 선을 찾는 분류기입니다. 커널을 바꾸면 직선뿐만 아니라 곡선 경계도 학습할 수 있어, 복잡한 데이터 패턴에도 강력하게 사용됩니다.

---

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

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| SVM 핵심 개념 | StatQuest | [Support Vector Machines, Clearly Explained!!!](https://www.youtube.com/watch?v=efR1C6CvhmE) |
| Kernel Trick (RBF) | StatQuest | [Support Vector Machines - The Polynomial Kernel](https://www.youtube.com/watch?v=Toet3EiSFcM) |
| C 파라미터 / 마진 | StatQuest | [Support Vector Machines - The Soft Margin](https://www.youtube.com/watch?v=IpKLTFGVMzs) |
