# Chapter 02. Cross Validation을 쉽게 이해하기

> 💡 **쉽게 이해하기**: 시험을 한 번만 보면 운이 작용할 수 있습니다. K-Fold는 데이터를 5등분하여 5번 번갈아 시험을 보고 평균 점수를 내는 방법입니다. 한 번의 우연보다 훨씬 공정하게 모델 성능을 평가할 수 있습니다.

---

`CrossValid.py`의 핵심은 "한 번 나눠서 평가하지 말고 여러 번 나눠 평균을 보자"입니다.

### 왜 필요한가?
- 단일 train/test split은 운에 따라 점수가 흔들릴 수 있음
- K-Fold는 데이터를 K개로 나눠 번갈아 검증하여 안정적인 평균 점수 제공

### 코드에서 보는 포인트
- `make_classification`: 실습용 분류 데이터 자동 생성
- `LogisticRegression`: 빠르고 해석이 쉬운 선형 분류기
- `cross_val_score(..., cv=5)`: 5번 반복 검증

### API로 확장 시 장점
- 실시간으로 `n_samples`, `n_features`, `cv`를 바꿔 결과 비교 가능
- 프론트에서 하이퍼파라미터 실험 UI를 만들기 쉬움

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| Cross Validation | StatQuest | [Machine Learning Fundamentals: Cross Validation](https://www.youtube.com/watch?v=fSytzGwwBVw) |
| Logistic Regression | StatQuest | [Logistic Regression, Clearly Explained](https://www.youtube.com/watch?v=yIYKR4sgzI8) |
| scikit-learn | freeCodeCamp | [Machine Learning with Python and Scikit-Learn](https://www.youtube.com/watch?v=hDKCxebp88A) |
