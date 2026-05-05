# Chapter 11. KMeans Clustering — 비지도 군집화

> 💡 **쉽게 이해하기**: 레이블(정답 라벨) 없이 비슷한 데이터끼리 자동으로 그룹을 만드는 방법입니다. 마치 색깔 펜 없이 사탕을 비슷한 것끼리 모아 K개의 그룹으로 나누는 것과 같습니다. 주가 종목 섹터 자동 분류나 고객 유형 분류에 활용됩니다.

---

### 핵심 개념

KMeans는 레이블 없이 데이터를 **K개의 군집(cluster)**으로 나누는 **비지도 학습** 알고리즘입니다.

각 군집 중심(centroid)을 반복적으로 이동하며 다음을 최소화합니다:

$$\text{Inertia} = \sum_{i} \min_{c \in C} \|x_i - c\|^2$$

### 구현 흐름

1. `make_blobs`로 다중 클러스터 가상 데이터 생성
2. `StandardScaler`로 스케일 정규화
3. `KMeans(n_clusters=K)` 학습
4. Silhouette Score로 군집 품질 평가
5. Elbow Method로 최적 K 탐색

### 주요 파라미터

| 파라미터 | 설명 |
|--------|------|
| `n_clusters` | 군집 수 K |
| `n_init` | 초기화 반복 횟수 (안정성 향상) |
| `cluster_std` | 데이터 분산 (클수록 군집 경계 불명확) |

### Silhouette Score

- **범위**: −1 ~ 1
- **1에 가까울수록** 군집이 잘 분리됨
- **0 근처**: 군집 경계가 모호
- **음수**: 잘못된 군집 배정

### API로 확장 시 장점

- 사용자가 K를 바꿔가며 Elbow 그래프 실시간 확인
- Silhouette Score와 Inertia를 동시에 시각화

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| KMeans Clustering | StatQuest | [K-means Clustering](https://www.youtube.com/watch?v=4b5d3muPQmA) |
| Silhouette Score | StatQuest | [Silhouette Analysis for K-Means](https://www.youtube.com/watch?v=InFNAGc1hZc) |
| Elbow Method | Normalized Nerd | [K-Means Clustering - Elbow Method](https://www.youtube.com/watch?v=4OEsJGPNPSo) |
| 비지도 학습 개념 | 3Blue1Brown | [Neural Networks - Unsupervised Learning](https://www.youtube.com/watch?v=aircAruvnKk) |
