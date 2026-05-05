from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import numpy as np

# ✅ 1. 가상 이진 분류 데이터 생성
X, y = make_classification(
    n_samples=1000,      # 샘플 수
    n_features=10,       # 특성 수
    n_informative=5,     # 유의미한 특성 수
    n_redundant=2,       # 중복된 특성 수
    n_classes=2,         # 이진 분류
    random_state=42
)

# ✅ 2. 모델 정의
model = LogisticRegression(max_iter=1000)

# ✅ 3. 5-Fold 교차검증
scores = cross_val_score(model, X, y, cv=5)

# ✅ 4. 결과 출력
print("각 Fold의 정확도:", scores)
print("평균 정확도:", np.mean(scores))
