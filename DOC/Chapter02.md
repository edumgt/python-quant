# Chapter 02. Cross Validation을 쉽게 이해하기 / Understanding Cross Validation

---

## 🇰🇷 한국어

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

## 🇺🇸 English

The key idea in `CrossValid.py`: "Don't evaluate with a single split — average across multiple splits."

### Why Is It Needed?
- A single train/test split can have high variance depending on which samples end up in which set
- K-Fold splits data into K parts, cycling through each as the validation set for a stable average score

### Code Highlights
- `make_classification`: automatically generates classification data for practice
- `LogisticRegression`: fast and interpretable linear classifier
- `cross_val_score(..., cv=5)`: runs 5 validation rounds

### API Extension Benefits
- Change `n_samples`, `n_features`, `cv` in real time and compare results
- Easy to build a hyperparameter experiment UI on the frontend

