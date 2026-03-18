# Chapter 11. KMeans Clustering — 비지도 군집화 / Unsupervised Clustering

---

## 🇰🇷 한국어

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

## 🇺🇸 English

### Core Concept

KMeans is an **unsupervised learning** algorithm that partitions data into **K clusters** without labels.

It iteratively moves cluster centroids to minimize:

$$\text{Inertia} = \sum_{i} \min_{c \in C} \|x_i - c\|^2$$

### Implementation Flow

1. Generate multi-cluster data with `make_blobs`
2. Normalize with `StandardScaler`
3. Fit `KMeans(n_clusters=K)`
4. Evaluate quality with Silhouette Score
5. Find optimal K with the Elbow Method

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `n_clusters` | Number of clusters K |
| `n_init` | Re-initialization runs (improves stability) |
| `cluster_std` | Data spread (higher → less distinct clusters) |

### Silhouette Score

- **Range**: −1 to 1
- **Close to 1**: well-separated clusters
- **Near 0**: overlapping cluster boundaries
- **Negative**: likely misassigned points

### API Extension Benefits

- Users can change K interactively and see the elbow plot update in real time
- Silhouette Score and Inertia displayed simultaneously
