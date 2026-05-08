<div align="center">

# 🐍 Python → 퀀트 시스템 개발 완전 로드맵

---
투자분석 기초 방법론	
- 매크로 분석: 경제지표 분석(금리, 물가, 유가 등 주요 지표 보는 법 ), 거시경제상황 분석 실습 

![alt text](image.png)


- 산업 분석: 산업 경쟁력 분석(산업경쟁력 개념/분석모형, 산업별 분석방법), 산업 분석 실습 
- 기본적 분석: 재무제표분석 (손익계산서/대차대조표/현금흐름표), 기업가치분석(상대가치평가 밸류에이션(멀티플), 절대가치평가 밸류에이션 (DCF, EVA, FCF 등)), 분석기업선정 및 밸류에이션 실습 
- 기술적 분석: 추세 분석(지지선과 저항선, 이동평균선, 갭 반전, 되돌림 분석 등), 패턴 분석, 캔들 차트 분석, 지표 분석, 앨리어트파동이론, 분석기업선정 및 기술적 분석
---

**퀀트 데이터 분석부터 알고리즘 트레이딩 시스템까지 — 실습 중심 교육 플랫폼**

**From Quant Data Analysis to Algorithmic Trading System — Hands-on Education Platform**

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa?logo=github-sponsors)](https://github.com/sponsors/edumgt)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[**English README**](README.en.md) | [**📚 챕터 문서**](DOC/) | [**📖 퀀트 용어 사전**](docs/Chapter20.md)

</div>

---

| ◀ 이전 강의 | 📚 커리큘럼 (7 / 10) | 다음 강의 ▶ |
|:---|:---:|---:|
| [← OpenStack 프라이빗 클라우드](https://github.com/edumgt/openstack-private-cloud) | **Python 퀀트 시스템** | [Python 트레이딩 샘플 →](https://github.com/edumgt/python-trading-sample) |

---

## 🗺️ 전체 로드맵 / Full Roadmap

```mermaid
flowchart TD
    P1["🟩 Phase 1 — 데이터 분석 기초<br/>Data Analysis<br/>pandas · numpy · matplotlib · 금융 데이터 수집"]
    P2["🟨 Phase 2 — 투자 이론 & 기술 분석<br/>Investment Theory<br/>이동평균 · RSI · 재무제표 · 밸류에이션"]
    P3["🟧 Phase 3 — 머신러닝 기초 ★Lab<br/>ML Fundamentals<br/>회귀 · 분류 · 교차검증 · 결정경계 시각화"]
    P4["🟥 Phase 4 — 퀀트 전략 & 백테스팅<br/>Quant Strategy<br/>추세추종 · 모멘텀 · 포트폴리오 최적화 · MDD/샤프"]
    P5["🟪 Phase 5 — 고급 ML/DL & 예측 모델 ★Lab<br/>Advanced ML/DL<br/>SVM · RandomForest · MLP · 시계열 · NLP 감성분석"]
    P6["🔴 Phase 6 — 자동매매 시스템 ★Lab<br/>Algorithmic Trading<br/>FastAPI 서비스 · 증권사 API · 실전 배포"]

    P1 --> P2 --> P3 --> P4 --> P5 --> P6

    style P1 fill:#1e5f3a,color:#fff,stroke:#4ae290,stroke-width:2px
    style P2 fill:#5f5f1e,color:#fff,stroke:#e2c44a,stroke-width:2px
    style P3 fill:#5f3a1e,color:#fff,stroke:#e2884a,stroke-width:2px
    style P4 fill:#5f1e1e,color:#fff,stroke:#e24a4a,stroke-width:2px
    style P5 fill:#3a1e5f,color:#fff,stroke:#884ae2,stroke-width:2px
    style P6 fill:#5f1e2d,color:#fff,stroke:#e24a6a,stroke-width:2px
```

> 📖 퀀트 용어가 낯설다면 [Chapter20 — 퀀트 투자 핵심 용어 가이드](docs/Chapter20.md)를 먼저 읽어보세요.

---

## ⚡ 실전 4단계 퀀트 로드맵 (Quick Path)

> 🎯 **가장 빠른 경로**: 데이터 → 전략 → 백테스트 → ML → 자동매매  
> 전체 Phase 1~6가 벅차다면 이 4단계 경로로 먼저 시작하세요.

```mermaid
flowchart LR
    S1["🟦 1단계 (2~3주)\nPython + 데이터\nyfinance · pandas\nOHLCV 처리"]
    S2["🟩 2단계 (3~4주)\n투자 전략\nMA · RSI · 볼린저\n규칙 기반 신호"]
    S3["🟨 3단계 (2~3주)\n백테스트 핵심\nCAGR · Sharpe\nMDD 검증"]
    S4["🟥 4단계 (4주+)\nML 고도화\nRandomForest\n자동매매 연결"]

    S1 --> S2 --> S3 --> S4

    style S1 fill:#1e3a5f,color:#fff,stroke:#4a90e2,stroke-width:2px
    style S2 fill:#1e5f3a,color:#fff,stroke:#4ae290,stroke-width:2px
    style S3 fill:#5f5f1e,color:#fff,stroke:#e2c44a,stroke-width:2px
    style S4 fill:#5f1e1e,color:#fff,stroke:#e24a4a,stroke-width:2px
```

| 단계 | 기간 | 핵심 목표 | 주요 도구 | 실습 파일 |
|------|------|-----------|-----------|-----------|
| **1단계** | 2~3주 | 데이터를 자유롭게 다루기 | `yfinance` · `pandas` · `matplotlib` | `QuantPipeline.py` |
| **2단계** | 3~4주 | 규칙 기반 매매 전략 1개 만들기 | `pandas rolling()` · RSI · 볼린저 | `QuantPipeline.py` |
| **3단계** | 2~3주 | 전략이 진짜 돈 되는지 검증 | CAGR · Sharpe · MDD · 승률 | `Backtest.py` |
| **4단계** | 4주+ | ML로 예측 정확도 높이기 + 자동매매 | `scikit-learn` · Alpaca · KIS API | `QuantPipeline.py` |

**🚀 4단계 첫 실행:**
```bash
python QuantPipeline.py   # 4단계 통합 실행 → quant_pipeline_result.png 생성
python Backtest.py        # 백테스트 상세 분석 → backtest_result.png 생성
python RiskManager.py     # 리스크 분석 → risk_result.png 생성
python PortfolioOptimizer.py  # 포트폴리오 최적화 → portfolio_result.png 생성
```

> 📘 **상세 가이드**: [DOC/Chapter16.md — 4단계 실전 로드맵 전체 코드](DOC/Chapter16.md)

---

## 📚 커리큘럼 상세 / Detailed Curriculum

---

### 🟩 Phase 1 — 데이터 분석 기초 (Data Analysis)

> 목표: 금융 데이터를 수집·정제·시각화하는 능력 확보

| # | 주제 | 핵심 라이브러리 | 퀀트 실습 |
|---|------|----------------|-----------|
| P1-1 | 배열 연산 | `numpy` | 수익률 계산, 로그 수익률 |
| P1-2 | 데이터프레임 | `pandas` | OHLCV 데이터 처리 |
| P1-3 | 시각화 | `matplotlib`, `seaborn` | 주가 차트, 수익률 히스토그램 |
| P1-4 | 금융 데이터 수집 | `yfinance`, `FinanceDataReader` | 글로벌·국내 주가 다운로드 |
| P1-5 | 데이터 전처리 | `pandas` | 결측치 처리, 정규화 |

**핵심 코드 예시:**
```python
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

df = fdr.DataReader('005930', '2020-01-01')  # 삼성전자
df['Close'].plot(title='삼성전자 주가')
plt.show()
```

---

### 🟨 Phase 2 — 투자 이론 & 기술 분석 (Investment Theory)

> 목표: 차트 지표와 재무 지표를 코드로 직접 계산·해석

| # | 주제 | 내용 | 관련 용어 |
|---|------|------|-----------|
| P2-1 | 이동평균 & 골든/데드크로스 | MA5/20/60/120, 매매 신호 | [이동평균선 →](docs/Chapter20.md) |
| P2-2 | RSI & 볼린저 밴드 | 과매수/과매도 판단 | [RSI →](docs/Chapter20.md) |
| P2-3 | 캔들 차트 분석 | 양봉/음봉, 패턴 인식 | [캔들 차트 →](docs/Chapter20.md) |
| P2-4 | 재무제표 수집 | PER, PBR, ROE 계산 | [기본적 분석 →](docs/Chapter20.md) |
| P2-5 | 밸류에이션 | DCF 모델, 상대가치 | [밸류에이션 →](docs/Chapter20.md) |
| P2-6 | 거시지표 해석 | 금리·환율·유가와 주식 관계 | [거시경제 →](docs/Chapter20.md) |
| P2-7 | **TradingView & Pine Script** | 멀티 자산 차트 분석, 보조지표·전략 코딩, 웹훅 연동 | [Ch.15 →](DOC/Chapter15.md) |

**핵심 코드 예시:**
```python
# RSI 계산
delta = df['Close'].diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = -delta.clip(upper=0).rolling(14).mean()
rsi = 100 - (100 / (1 + gain / loss))
```

---

### 🟧 Phase 3 — 머신러닝 기초 (ML Fundamentals) `[Lab]`

> 목표: scikit-learn으로 주가 방향 예측 모델 구축의 기초 이해

| Chapter | 주제 | 스크립트 | 퀀트 적용 |
|---------|------|----------|-----------|
| [Ch.02](DOC/Chapter02.md) | 교차 검증 | `CrossValid.py` | 전략 과최적화(overfitting) 방지 |
| [Ch.03](DOC/Chapter03.md) | 결정경계 시각화 | `DecisionBoundary.py` | 매수/매도 구간 시각화 |
| [Ch.04](DOC/Chapter04.md) | 선형·다항 회귀 | `LinearRegression.py` | 가격 예측, 추세선 모델링 |
| — | 특징 공학 | — | 기술 지표 → ML 입력 피처 변환 |

**핵심 퀀트 연결:**
```python
from sklearn.model_selection import cross_val_score
# 교차 검증으로 백테스트 신뢰도 검증
scores = cross_val_score(model, X_features, y_direction, cv=5)
print(f'평균 정확도: {scores.mean():.2%}')
```

---

### 🟥 Phase 4 — 퀀트 전략 & 백테스팅 (Quant Strategy)

> 목표: 실제 투자 전략을 코드로 구현하고 성과를 정량 평가

| # | 전략 | 내용 | 성과 지표 |
|---|------|------|-----------|
| P4-1 | 추세추종 | 이동평균 크로스오버 | 연간 수익률, MDD |
| P4-2 | 모멘텀 | 12개월 수익률 기반 종목 선택 | 샤프 비율 |
| P4-3 | 평균회귀 | 볼린저 밴드 이탈 전략 | 승률, 손익비 |
| P4-4 | 포트폴리오 최적화 | Mean-Variance, Risk Parity | 변동성, 상관계수 |
| P4-5 | 백테스트 구현 | `backtrader` / 직접 구현 | [MDD →](docs/Chapter20.md) · [샤프 →](docs/Chapter20.md) |
| P4-6 | 계절성 분석 | 1월 효과, 연말 랠리 탐지 | [계절성 →](docs/Chapter20.md) |

**핵심 코드 예시:**
```python
# 샤프 비율 계산
def sharpe_ratio(returns, risk_free=0.03):
    excess = returns - risk_free / 252
    return excess.mean() / excess.std() * (252 ** 0.5)

# MDD 계산
def max_drawdown(equity_curve):
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    return drawdown.min()
```

> ⚠️ 백테스트 주의: 과거 성과 ≠ 미래 수익. 항상 워크포워드 테스트와 교차 검증을 병행하세요.

---

### 🟪 Phase 5 — 고급 ML/DL & 예측 모델 (Advanced ML/DL) `[Lab]`

> 목표: 앙상블·딥러닝·NLP로 퀀트 예측 모델을 고도화

| Chapter | 주제 | 스크립트 | 퀀트 적용 |
|---------|------|----------|-----------|
| [Ch.11](DOC/Chapter11.md) | KMeans 클러스터링 | `KMeansClustering.py` | 주식 섹터 자동 분류, 포트폴리오 분산화 |
| [Ch.12](DOC/Chapter12.md) | SVM 분류기 | `SVMClassifier.py` | 주가 방향(상승/하락) 분류 |
| [Ch.04](DOC/Chapter04.md) | 랜덤 포레스트 | `RandomForest.py` | 팩터 중요도 분석, 앙상블 예측 |
| [Ch.13](DOC/Chapter13.md) | MLP 신경망 | `NeuralNetMLP.py` | 비선형 가격 패턴 학습 |
| [Ch.14](DOC/Chapter14.md) | NLP 감성 분석 | `SentimentAnalysis.py` | 뉴스 감성 → 투자 신호 생성 |
| [Ch.05](DOC/Chapter05.md) | 시계열 예측 | `(ARIMA / LSTM 확장)` | ARIMA → LSTM 순차 예측 |
| [Ch.06](DOC/Chapter06.md) | 생성형 AI | `HuggingFaceGPU.py` | LLM 기반 리포트 요약·분석 |

**ML → 퀀트 파이프라인:**
```mermaid
flowchart LR
    subgraph Features["📊 기술 지표 피처"]
        F1["MA · RSI · Volume"]
        F2["PER · PBR · ROE"]
        F3["뉴스 텍스트"]
    end
    subgraph Models["🤖 ML 모델"]
        M1["RandomForest"]
        M2["SVM"]
        M3["TF-IDF + LR"]
    end
    subgraph Signals["📈 퀀트 신호"]
        S1["매수(1) / 매도(0)"]
        S2["가치주 스크리닝"]
        S3["감성 점수 → 포지션 조절"]
    end
    F1 --> M1 --> S1
    F2 --> M2 --> S2
    F3 --> M3 --> S3
    style M1 fill:#1e5f3a,color:#fff
    style M2 fill:#1e3a5f,color:#fff
    style M3 fill:#3a1e5f,color:#fff
```

---

### 🔴 Phase 6 — 자동매매 시스템 (Algorithmic Trading) `[Lab]`

> 목표: ML 모델을 실시간 API 서비스로 만들고 증권사 API에 연결

| Chapter | 주제 | 스크립트 | 내용 |
|---------|------|----------|------|
| [Ch.07](DOC/Chapter07.md) | FastAPI 백엔드 | `app/backend/main.py` | REST API 서버로 모델 서빙 |
| [Ch.08](DOC/Chapter08.md) | Vanilla JS 프론트 | `app/frontend/` | 실시간 대시보드 UI |
| [Ch.09](DOC/Chapter09.md) | 클라우드 배포 | — | AWS/GCP 배포, Docker 컨테이너화 |
| [Ch.10](DOC/Chapter10.md) | 실습 과제 | — | 종합 퀀트 시스템 구축 |
| — | 증권사 API 연결 | — | [KIS·키움·Binance →](docs/Chapter20.md) |
| — | 알고리즘 트레이딩 | — | [추세·평균회귀·차익거래 →](docs/Chapter20.md) |

**시스템 아키텍처:**
```mermaid
flowchart LR
    DC["🗄️ 데이터 수집<br/>yfinance · 크롤링"]
    ML["🤖 ML 예측<br/>모델 추론 · 신호 생성"]
    API["⚡ FastAPI 서버<br/>/api/ml/predict<br/>실시간 대시보드"]
    BRK["🏦 증권사 API<br/>매수/매도 주문<br/>포지션 관리"]

    DC --> ML --> API --> BRK

    style DC fill:#1a3a5c,color:#fff,stroke:#4a90e2
    style ML fill:#1a5c3a,color:#fff,stroke:#4ae290
    style API fill:#5c3a1a,color:#fff,stroke:#e2884a
    style BRK fill:#5c1a1a,color:#fff,stroke:#e24a4a
```

---

---

## 📋 챕터별 실습 스크립트 / Chapter Script Index

> ML/DL Lab 각 챕터와 실행 스크립트, 추천 YouTube 강의를 한 곳에 정리했습니다.

| 챕터 | 주제 | 스크립트 | 📺 추천 YouTube |
|------|------|---------|----------------|
| 01 | 저장소 구성 및 학습 전략 | — | [🎬 머신러닝 학습 로드맵](https://www.youtube.com/results?search_query=머신러닝+학습+로드맵+파이썬+한국어) |
| 02 | Cross Validation 이해 | `CrossValid.py` | [🎬 K-Fold 교차검증 설명](https://www.youtube.com/results?search_query=K-Fold+교차검증+파이썬+머신러닝+한국어) |
| 03 | Decision Boundary 시각화 | `DecisionBoundary.py` | [🎬 결정경계 시각화 강의](https://www.youtube.com/results?search_query=결정경계+시각화+머신러닝+파이썬+한국어) |
| 04 | Random Forest 결과 해석 | `RandomForest.py` | [🎬 랜덤포레스트 한국어 강의](https://www.youtube.com/results?search_query=랜덤포레스트+파이썬+머신러닝+한국어+설명) |
| 05 | OpenCV 영상 생성 | `OpenCVCPU.py` | [🎬 OpenCV 파이썬 기초](https://www.youtube.com/results?search_query=OpenCV+파이썬+영상처리+기초+한국어) |
| 06 | HuggingFace Diffusers | `HuggingFaceGPU.py` | [🎬 HuggingFace Stable Diffusion](https://www.youtube.com/results?search_query=HuggingFace+Stable+Diffusion+파이썬+한국어+강의) |
| 07 | FastAPI 백엔드 구조 | `app/backend/main.py` | [🎬 FastAPI 한국어 강의](https://www.youtube.com/results?search_query=FastAPI+파이썬+REST+API+백엔드+한국어) |
| 08 | Vanilla JS 프론트엔드 모듈 | `app/frontend/` | [🎬 Vanilla JS 프론트엔드](https://www.youtube.com/results?search_query=Vanilla+JavaScript+프론트엔드+DOM+한국어) |
| 09 | 클라우드 배포 시나리오 | — | [🎬 파이썬 앱 클라우드 배포](https://www.youtube.com/results?search_query=파이썬+FastAPI+클라우드+배포+AWS+한국어) |
| 10 | 실습 과제 목록 | — | [🎬 머신러닝 프로젝트 실습](https://www.youtube.com/results?search_query=머신러닝+프로젝트+실습+파이썬+포트폴리오+한국어) |
| 11 | KMeans 비지도 클러스터링 | `KMeansClustering.py` | [🎬 KMeans 클러스터링 설명](https://www.youtube.com/results?search_query=KMeans+클러스터링+파이썬+비지도학습+한국어) |
| 12 | SVM 분류기 | `SVMClassifier.py` | [🎬 SVM 서포트벡터머신](https://www.youtube.com/results?search_query=SVM+서포트벡터머신+파이썬+분류+한국어) |
| 13 | MLP 신경망 | `NeuralNetMLP.py` | [🎬 MLP 다층퍼셉트론 신경망](https://www.youtube.com/results?search_query=MLP+다층퍼셉트론+신경망+파이썬+딥러닝+한국어) |
| 14 | NLP 텍스트 분류 | `SentimentAnalysis.py` | [🎬 TF-IDF 텍스트 분류](https://www.youtube.com/results?search_query=TF-IDF+텍스트분류+NLP+파이썬+한국어) |
| 15 | TradingView & Pine Script | — | [🎬 Pine Script 퀀트 전략](https://www.youtube.com/results?search_query=PineScript+TradingView+퀀트+전략+한국어) |
| 16 | 퀀트 실전 4단계 로드맵 | `QuantPipeline.py` | [🎬 퀀트 자동매매 파이썬](https://www.youtube.com/results?search_query=퀀트+자동매매+파이썬+백테스트+한국어) |
| 17 | 1D CNN 시계열 패턴 분류 | `CNNTimeSeries.py` | [🎬 CNN 시계열 분류](https://www.youtube.com/results?search_query=1D+CNN+시계열+파이썬+딥러닝+한국어) |
| 18 | LSTM 주가 수익률 예측 | `LSTMPredictor.py` | [🎬 LSTM 주가 예측 파이썬](https://www.youtube.com/results?search_query=LSTM+주가+예측+파이썬+딥러닝+한국어) |
| 19 | Transformer 시계열 멀티스텝 예측 | `TransformerTimeSeries.py` | [🎬 Transformer 시계열 예측](https://www.youtube.com/results?search_query=Transformer+시계열+예측+파이썬+딥러닝+한국어) |
| 20 | 퀀트 핵심 용어 가이드 & 자격증 | — | [🎬 퀀트 투자 용어 사전](https://www.youtube.com/results?search_query=퀀트+투자+용어+금융+한국어+강의) |
| 21 | 퀀트 마스터 로드맵 Python 실전 | — | [🎬 퀀트 파이썬 실전 코드](https://www.youtube.com/results?search_query=퀀트+파이썬+자동매매+백테스트+실전+한국어) |

## 🗂️ 저장소 구조 / Repository Structure

```text
.
├── QuantPipeline.py        # ★ 4단계 통합 파이프라인 (데이터→전략→백테스트→ML)
├── Backtest.py             # 백테스트 엔진 (MA 크로스오버, CAGR·Sharpe·MDD)
├── RiskManager.py          # 리스크 관리 (손절선·VaR·포지션 사이징)
├── PortfolioOptimizer.py   # 포트폴리오 최적화 (Mean-Variance·Risk Parity)
├── CrossValid.py           # Phase 3: K-Fold 교차 검증
├── DecisionBoundary.py     # Phase 3: 결정경계 시각화
├── LinearRegression.py     # Phase 3: 선형·다항 회귀
├── RandomForest.py         # Phase 5: 랜덤 포레스트 (팩터 분석)
├── KMeansClustering.py     # Phase 5: 섹터 클러스터링
├── SVMClassifier.py        # Phase 5: 방향 분류
├── NeuralNetMLP.py         # Phase 5: MLP 신경망
├── SentimentAnalysis.py    # Phase 5: 뉴스 감성 분석
├── OpenCVCPU.py            # Phase 5: 차트 패턴 인식 (OpenCV)
├── HuggingFaceGPU.py       # Phase 5: 생성형 AI (GPU)
├── requirements.txt
├── docs/
│   ├── Chapter20.md        # 📖 퀀트 투자 핵심 용어 가이드 & 자격증
│   ├── Chapter21.md        # 🐍 퀀트 마스터 로드맵 Python 실전 코드 (초급/중급/고급)
│   └── ...                 # (Chapter01~19, day006~day099, 기타)
├── DOC/
│   ├── Chapter01.md        # 저장소 전체 지도 & 학습 전략
│   ├── Chapter02.md        # Cross Validation
│   ├── Chapter03.md        # Decision Boundary
│   ├── Chapter04.md        # Random Forest
│   ├── Chapter05.md        # OpenCV 영상 처리
│   ├── Chapter06.md        # HuggingFace 생성형 AI
│   ├── Chapter07.md        # FastAPI 백엔드
│   ├── Chapter08.md        # Vanilla JS 프론트엔드
│   ├── Chapter09.md        # 클라우드 배포
│   ├── Chapter10.md        # 실습 과제
│   ├── Chapter11.md        # KMeans Clustering
│   ├── Chapter12.md        # SVM Classifier
│   ├── Chapter13.md        # MLP Neural Network
│   ├── Chapter14.md        # NLP Text Classification
│   ├── Chapter15.md        # TradingView & Pine Script
│   └── Chapter16.md        # ★ 퀀트 4단계 로드맵 (데이터→전략→백테스트→ML→자동매매)
└── app/
    ├── backend/
    │   └── main.py         # FastAPI 서버 (전체 엔드포인트)
    └── frontend/
        ├── index.html
        ├── styles.css
        └── js/
            ├── app.js · api.js
            └── views/      # 각 실습별 UI 모듈
```

---

## 🚀 빠른 시작 / Quick Start

### Python 환경

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. FastAPI 서버 실행
uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload

# 3. 브라우저 접속
# http://localhost:8000
```

### Node.js 개발 서버

```bash
cd app/frontend
npm install
npm run dev     # http://localhost:3000
```

### 독립 스크립트 실행

```bash
# ★ 4단계 통합 파이프라인 (첫 실행 추천)
python QuantPipeline.py          # 데이터→전략→백테스트→ML → quant_pipeline_result.png

# 퀀트 분석 스크립트
python Backtest.py               # 백테스트 엔진 (MA 크로스오버) → backtest_result.png
python RiskManager.py            # 리스크 분석 (VaR·손절·포지션) → risk_result.png
python PortfolioOptimizer.py     # 포트폴리오 최적화 → portfolio_result.png

# Phase 3 — ML 기초
python CrossValid.py
python DecisionBoundary.py
python LinearRegression.py

# Phase 5 — 고급 ML/DL
python KMeansClustering.py
python SVMClassifier.py
python RandomForest.py
python NeuralNetMLP.py
python SentimentAnalysis.py
```

---

## 📡 API 엔드포인트 / API Endpoints

| Method | Endpoint | 설명 | 퀀트 용도 |
|--------|----------|------|-----------|
| `GET`  | `/api/health` | 서버 상태 확인 | — |
| `POST` | `/api/ml/cross-validation` | K-Fold 교차 검증 | 전략 신뢰도 검증 |
| `GET`  | `/api/ml/decision-boundary` | 결정경계 시각화 | 매수/매도 구간 확인 |
| `POST` | `/api/ml/linear-regression` | 선형·다항 회귀 | 가격 추세 예측 |
| `POST` | `/api/ml/random-forest` | 랜덤 포레스트 | 팩터 중요도 & 방향 예측 |
| `POST` | `/api/ml/kmeans` | KMeans 클러스터링 | 종목 섹터 자동 분류 |
| `POST` | `/api/ml/svm` | SVM 분류 | 상승/하락 신호 생성 |
| `POST` | `/api/ml/mlp` | MLP 신경망 | 비선형 패턴 학습 |
| `POST` | `/api/nlp/text-classify` | TF-IDF 감성 분류 | 뉴스 → 투자 신호 |
| `POST` | `/api/cv/circle-animation` | OpenCV 영상 | 차트 패턴 시각화 |
| `POST` | `/api/genai/text-to-image` | Stable Diffusion | — (GPU 필요) |

전체 Swagger 문서: `http://localhost:8000/docs`

---

## 🎓 학습 체크리스트 / Learning Checklist

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ★ 4단계 실전 경로 (QuantPipeline.py / DOC/Chapter16.md)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1단계 — Python + 데이터 (2~3주)
  [ ] yfinance로 AAPL, QQQ, SPY, 삼성전자(.KS) 다운로드
  [ ] OHLCV 의미 이해 (시가·고가·저가·종가·거래량)
  [ ] pct_change()로 일별 수익률 계산
  [ ] rolling().mean()으로 MA20·MA60 추가
  [ ] matplotlib으로 주가·거래량·누적수익률 3패널 차트

2단계 — 투자 전략 만들기 (3~4주)
  [ ] 이동평균 골든크로스/데드크로스 signal 컬럼 생성
  [ ] RSI 14일 직접 구현 (과매수/과매도 표시)
  [ ] 볼린저 밴드 (20일, 2σ) 계산
  [ ] MACD (12/26/9) 히스토그램 차트
  [ ] 전략 신호를 차트에 매수▲/매도▼ 마커로 표시

3단계 — 백테스트 핵심 (2~3주)
  [ ] CAGR, Sharpe Ratio, MDD, 승률 계산 함수 작성
  [ ] position = signal.shift(1) 로 미래 데이터 누수 방지
  [ ] 전략 vs Buy&Hold 누적 수익률 비교 차트
  [ ] Sharpe > 1.0 & MDD > -15% 합격 기준 체크
  [ ] Backtest.py 실행 → backtest_result.png 확인
  [ ] fast/slow 파라미터 변경하며 최적 조합 탐색

4단계 — ML + 자동매매 (4주+)
  [ ] 기술 지표 8개+ 를 ML 피처로 변환
  [ ] TimeSeriesSplit으로 미래 누수 없이 교차검증
  [ ] RandomForest 피처 중요도 분석
  [ ] QuantPipeline.py 실행 → quant_pipeline_result.png 확인
  [ ] Alpaca 계좌 생성 → Paper Trading 연결
  [ ] 또는 KIS API 모의투자 연결

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 1~6 전체 경로
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1  [ ] yfinance로 삼성전자 주가 다운로드
         [ ] 주가 차트 그리기 (matplotlib)

Phase 2  [ ] 이동평균선 + 골든크로스 신호 코딩
         [ ] RSI 직접 계산 & 과매수/과매도 표시

Phase 3  [ ] CrossValid.py 실행 & 교차 검증 이해
         [ ] LinearRegression.py로 가격 회귀 모델 학습

Phase 4  [ ] Backtest.py 실행 → CAGR·Sharpe·MDD 확인
         [ ] RiskManager.py 실행 → VaR·손절선 분석
         [ ] PortfolioOptimizer.py → 효율적 프론티어 시각화

Phase 5  [ ] KMeans로 코스피 종목 클러스터링
         [ ] SentimentAnalysis로 뉴스 감성 점수 생성
         [ ] QuantPipeline.py → ML 방향 예측 정확도 확인

Phase 6  [ ] FastAPI 서버로 모델 API 서빙
         [ ] 증권사 API 연결 & 모의 주문 실행
         [ ] 텔레그램 알림 연동
```

---

## 💖 후원 / Sponsor

이 프로젝트가 도움이 되셨다면 GitHub Sponsors로 후원해 주세요!

후원금은 다음에 사용됩니다:
- ✨ 새로운 ML/DL 퀀트 예제 추가
- 📖 문서 품질 개선
- 🖥️ 클라우드 인프라 유지
- 🎓 교육 컨텐츠 확장

[![후원하기](https://img.shields.io/badge/GitHub%20Sponsors로%20후원하기-%E2%9D%A4-ea4aaa?logo=github-sponsors&style=for-the-badge)](https://github.com/sponsors/edumgt)

---

## 🤝 기여 / Contributing

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고해 PR을 보내주세요.

---

## 📄 라이선스 / License

[MIT License](LICENSE) © edumgt
