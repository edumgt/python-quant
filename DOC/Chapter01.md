# Chapter 01. 저장소 전체 지도와 학습 전략

> 💡 **쉽게 이해하기**: 이 저장소는 퀀트(알고리즘 트레이딩) 개발자가 되기 위한 **6단계 학습 로드맵**입니다. 파이썬 기초부터 자동매매 시스템까지, 각 단계를 실습 파일 하나씩 직접 실행하며 단계별로 성장할 수 있습니다.

---

이 저장소는 **파이썬 기초 → 데이터 분석 → 투자 이론 → ML/DL → 퀀트 전략 → 자동매매 시스템** 흐름으로 설계된 퀀트 개발 완전 로드맵입니다.

### 핵심 목표

- 코드 한 파일 단위로 실행 가능한 실습 경험 확보
- 모델 결과를 "숫자"와 "시각"으로 동시에 이해
- 로컬 스크립트를 API 서비스 형태로 확장하는 사고 훈련
- ML/DL 기법을 실제 퀀트 전략과 연결하는 능력 배양

### 6단계 학습 경로

#### Phase 0 — 파이썬 기초
코딩 경험 없이도 시작할 수 있는 파이썬 핵심 문법

#### Phase 1 — 데이터 분석
`pandas`, `numpy`, `matplotlib`으로 금융 데이터 수집·가공·시각화

#### Phase 2 — 투자 이론 & 기술 분석
이동평균, RSI, 재무제표, 밸류에이션을 코드로 직접 구현

#### Phase 3 — 머신러닝 기초 `[Lab 실습]`
| 순서 | 파일 | 퀀트 연결 |
|------|------|-----------|
| 1 | `CrossValid.py` | 전략 과최적화 방지 |
| 2 | `DecisionBoundary.py` | 매수/매도 구간 시각화 |
| 3 | `LinearRegression.py` | 주가 추세 모델링 |

#### Phase 4 — 퀀트 전략 & 백테스팅
추세추종, 모멘텀, 포트폴리오 최적화, MDD/샤프 비율 직접 구현

#### Phase 5 — 고급 ML/DL `[Lab 실습]`
| 순서 | 파일 | 퀀트 연결 |
|------|------|-----------|
| 4 | `KMeansClustering.py` | 종목 섹터 자동 분류 |
| 5 | `SVMClassifier.py` | 상승/하락 방향 분류 |
| 6 | `RandomForest.py` | 팩터 중요도 분석 |
| 7 | `NeuralNetMLP.py` | 비선형 가격 패턴 학습 |
| 8 | `SentimentAnalysis.py` | 뉴스 감성 → 투자 신호 |
| 9 | `OpenCVCPU.py` | 차트 패턴 인식 |
| 10 | `HuggingFaceGPU.py` | LLM 기반 리포트 분석 |

#### Phase 6 — 자동매매 시스템 `[Lab 실습]`
FastAPI 서비스, 증권사 API 연결, 실전 배포

### 학습 원칙

1. **퀀트 용어 먼저**: [README2.md 퀀트 용어 사전](../README2.md)으로 개념 정립 후 코드로 진입
2. **작게 시작**: 전략 하나를 간단히 구현하고 점진적으로 고도화
3. **과최적화 경계**: 백테스트가 좋아도 반드시 워크포워드 검증
4. **시스템 사고**: 단순 스크립트 → API 서비스 → 자동화로 단계 확장

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| Python 기초 | freeCodeCamp | [Python for Beginners - Full Course](https://www.youtube.com/watch?v=rfscVS0vtbw) |
| pandas | Keith Galli | [Complete Python Pandas Tutorial](https://www.youtube.com/watch?v=vmEHCJofslg) |
| numpy / matplotlib | freeCodeCamp | [Data Analysis with Python - Full Course](https://www.youtube.com/watch?v=r-uOLxNrNk8) |
| 머신러닝 입문 | StatQuest | [A Gentle Introduction to Machine Learning](https://www.youtube.com/watch?v=Gv9_4yMHFhI) |
| FastAPI | Tech With Tim | [FastAPI Tutorial](https://www.youtube.com/watch?v=7t2alSnE2-I) |
