# Chapter 01. 저장소 전체 지도와 학습 전략 / Repository Overview & Learning Strategy

---

## 🇰🇷 한국어

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

## 🇺🇸 English

This repository is a complete quant development roadmap: **Python basics → data analysis → investment theory → ML/DL → quant strategies → algorithmic trading system**.

### Core Goals

- Hands-on experience with each concept in a single runnable file
- Understand model results both numerically and visually
- Practice extending local scripts to API-based services
- Connect ML/DL techniques to real quant strategies

### 6-Phase Learning Path

#### Phase 0 — Python Fundamentals
Core Python syntax accessible to beginners with no prior coding experience

#### Phase 1 — Data Analysis
Collect, process, and visualize financial data with `pandas`, `numpy`, `matplotlib`

#### Phase 2 — Investment Theory & Technical Analysis
Implement moving averages, RSI, financial statements, and valuation models in code

#### Phase 3 — ML Fundamentals `[Lab]`
| Order | File | Quant Application |
|-------|------|-------------------|
| 1 | `CrossValid.py` | Prevent strategy overfitting |
| 2 | `DecisionBoundary.py` | Visualize buy/sell zones |
| 3 | `LinearRegression.py` | Price trend modeling |

#### Phase 4 — Quant Strategy & Backtesting
Implement trend-following, momentum, portfolio optimization, MDD/Sharpe ratio from scratch

#### Phase 5 — Advanced ML/DL `[Lab]`
| Order | File | Quant Application |
|-------|------|-------------------|
| 4 | `KMeansClustering.py` | Auto sector classification |
| 5 | `SVMClassifier.py` | Up/down direction classification |
| 6 | `RandomForest.py` | Factor importance analysis |
| 7 | `NeuralNetMLP.py` | Nonlinear price pattern learning |
| 8 | `SentimentAnalysis.py` | News sentiment → trading signals |
| 9 | `OpenCVCPU.py` | Chart pattern recognition |
| 10 | `HuggingFaceGPU.py` | LLM-based report analysis |

#### Phase 6 — Algorithmic Trading System `[Lab]`
FastAPI services, brokerage API integration, production deployment

### Learning Principles

1. **Vocabulary first**: Build concepts via [README2.md Quant Glossary](../README2.md) before touching code
2. **Start small**: Implement one simple strategy, then refine it incrementally
3. **Guard against overfitting**: Always walk-forward test even when backtest looks great
4. **Think in systems**: Simple script → API service → full automation
