# 투자분석 기초 방법론 — Python Quant Lab

> **모듈 7 완성 커리큘럼** | 매크로 → 산업 → 기본적 → 기술적 분석 → 통합 리포트  
> Python · FastAPI · Vanilla JS 풀스택 학습 환경

---

## 📚 커리큘럼 전체 구성

본 저장소의 `docs/` 디렉터리는 **모듈 7: 투자분석 기초 방법론** 10일 차 강의 자료를 담고 있습니다.  
각 문서는 이론 설명 → Python 실습 코드 → 웹앱 연계 → 해보기 활동 순서로 구성됩니다.

### 🗺️ 학습 로드맵

```
[매크로 분석] ──► [산업 분석] ──► [기본적 분석] ──► [기술적 분석] ──► [통합 리포트]
  Day 042~044       Day 045~046     Day 047~049       Day 050~051        Day 051 실습
  27~29.md          30~31.md        32~34.md           35~36.md           36.md §4
```

---

### 📋 Day별 학습 내용 상세

#### 📌 모듈 7-A: 매크로 분석 (거시경제)

| 파일 | Day | 주제 | 핵심 내용 | 웹앱 연계 |
|------|-----|------|-----------|-----------|
| [27.md](docs/27.md) | Day 042 | **매크로 분석 개요 및 금리 분석** | 기준금리·장단기 금리차·채권 수익률 곡선(Yield Curve)·GBM 시뮬레이션 | `/api/macro/realtime` |
| [28.md](docs/28.md) | Day 043 | **경제지표 분석 (물가·유가 등)** | CPI·PPI·PCE 인플레이션, WTI/브렌트 유가, USD/KRW 환율 상관분석 | `/api/macro/simulation` |
| [29.md](docs/29.md) | Day 044 | **거시경제 상황 분석 실습** | 경기사이클 4단계 분류, 자산군별 대응 전략, 멀티 지표 통합 대시보드 | macroRealtime.js · macroSimulation.js |

> **핵심 Python 라이브러리**: `yfinance`, `pandas`, `matplotlib`, `scipy`, `statsmodels`  
> **핵심 개념**: 기준금리, 인플레이션, 경기사이클, GBM, 상관관계 분석

---

#### 📌 모듈 7-B: 산업 분석

| 파일 | Day | 주제 | 핵심 내용 | 웹앱 연계 |
|------|-----|------|-----------|-----------|
| [30.md](docs/30.md) | Day 045 | **산업 분석 이론** | Porter's 5 Forces, PEST 분석, SWOT 분석, 산업 수명주기(Life Cycle), TAM/SAM/SOM | `/api/industry/porter` · `/api/industry/lifecycle` |
| [31.md](docs/31.md) | Day 046 | **산업 분석 실습** | 섹터 로테이션 전략, 업종별 KPI 비교, Peer Comparison 자동화, 공급망 분석 | `/api/industry/sector` · `/api/industry/peer` · industryAnalysis.js |

> **핵심 Python 라이브러리**: `yfinance`, `pandas`, `matplotlib`, `seaborn`, `plotly`  
> **핵심 개념**: Porter's 5 Forces, SWOT, 산업 수명주기, 섹터 로테이션, Peer Comparison

---

#### 📌 모듈 7-C: 기본적 분석 (Fundamental Analysis)

| 파일 | Day | 주제 | 핵심 내용 | 웹앱 연계 |
|------|-----|------|-----------|-----------|
| [32.md](docs/32.md) | Day 047 | **재무제표 분석 I** | 손익계산서(매출·영업이익·순이익), 대차대조표(자산·부채·자본), 수익성·안정성 비율 | `/api/dart/company-search` · financialStatement.js |
| [33.md](docs/33.md) | Day 048 | **재무제표 분석 II** | 현금흐름표(CFO·CFI·CFF), FCF·EVA·WACC 계산, DCF 내재가치 산출 | dartCompanySearch.js · valuation.js |
| [34.md](docs/34.md) | Day 049 | **상대가치 평가 (밸류에이션 멀티플)** | PER·PBR·PSR·EV/EBITDA 업종 비교, 목표주가 밴드, Bull/Base/Bear 시나리오 | `/api/quant/pipeline` · pipeline.js |

> **핵심 Python 라이브러리**: `yfinance`, `pykrx`, `pandas`, `matplotlib`, `reportlab`, `openpyxl`  
> **핵심 개념**: 손익계산서, 현금흐름표, DCF, EVA, FCF, WACC, PER, PBR, EV/EBITDA, 안전마진  
> **외부 API**: [DART Open API](https://opendart.fss.or.kr) (한국 기업 공시 데이터)

---

#### 📌 모듈 7-D: 기술적 분석 (Technical Analysis)

| 파일 | Day | 주제 | 핵심 내용 | 웹앱 연계 |
|------|-----|------|-----------|-----------|
| [35.md](docs/35.md) | Day 050 | **기술적 분석 I — 추세 & 지표** | 이동평균선(MA5·20·60·120), 골든/데드크로스, RSI·MACD·볼린저밴드, 지지선·저항선 | technicalChart.js (Tab 1~3·5) |
| [36.md](docs/36.md) | Day 051 | **기술적 분석 II — 패턴 & 엘리어트 파동** | 캔들 패턴(도지·망치·엔걸핑), 차트 패턴(H&S·이중천장·삼각수렴), 엘리어트 파동 이론 | technicalChart.js (Tab 4·6·7) |

> **핵심 Python 라이브러리**: `yfinance`, `mplfinance`, `pandas-ta`, `matplotlib`  
> **핵심 개념**: 캔들패턴, 헤드앤숄더, 이중천장·바닥, 엘리어트 파동, 피보나치 되돌림

---

#### 📌 모듈 7-E: 통합 리포트 (Integrated Report) — [36.md §4](docs/36.md)

Day 051 문서의 §4는 기본적·기술적 분석을 결합한 **실제 증권사 수준의 통합 투자 분석 리포트** 생성 실습입니다.

| 단계 | 내용 |
|------|------|
| Step 1 — 종목 선정 | 3단계 스크리닝 Funnel (시가총액·ROE·MA 필터) |
| Step 2 — 기본적 분석 | 5-Block 구조: 기업개요·재무제표·수익성·밸류에이션·리스크 |
| Step 3 — 기술적 분석 | 7항목 체크리스트: MA·RSI·MACD·BB·거래량·캔들·차트패턴 |
| Step 4 — 통합 스코어링 | 100점 매트릭스 → 강력매수/매수/중립/비중축소/매도 |
| Step 5 — 리포트 자동 생성 | `integrated_report()` 함수로 18×22 멀티패널 PNG 출력 |
| UI 제안 | Bloomberg Terminal 수준 3-패널 대시보드 (좌:FA / 중:차트 / 우:의견) |

---

## 🔗 웹앱 API — 전체 엔드포인트 맵

| 분류 | 엔드포인트 | 설명 | 연계 프론트 |
|------|-----------|------|------------|
| **공통** | `GET /api/health` | 서버 상태 확인 | — |
| **매크로** | `POST /api/macro/realtime` | 금리·환율·유가 실시간 분석 | macroRealtime.js |
| **매크로** | `POST /api/macro/simulation` | GBM 기반 시나리오 시뮬레이션 | macroSimulation.js |
| **산업** | `POST /api/industry/porter` | Porter's 5 Forces 점수화 | industryAnalysis.js |
| **산업** | `POST /api/industry/sector` | 섹터 로테이션 분석 | industryAnalysis.js |
| **산업** | `POST /api/industry/peer` | 동종 기업 Peer Comparison | industryAnalysis.js |
| **산업** | `POST /api/industry/lifecycle` | 산업 수명주기 분석 | industryAnalysis.js |
| **DART** | `POST /api/dart/company-search` | 기업 공시 검색 (DART API) | dartCompanySearch.js |
| **퀀트** | `POST /api/quant/backtest` | 이동평균 크로스오버 백테스트 | backtest.js |
| **퀀트** | `POST /api/quant/portfolio` | MPT 포트폴리오 최적화 | portfolio.js |
| **퀀트** | `POST /api/quant/risk` | VaR·CVaR·MDD 리스크 분석 | risk.js |
| **퀀트** | `POST /api/quant/pipeline` | 멀티팩터 퀀트 파이프라인 | pipeline.js |
| **재무** | — | 재무제표 시각화 (yfinance) | financialStatement.js · valuation.js |
| **ML** | `POST /api/ml/cross-validation` | 교차검증 | crossValidation.js |
| **ML** | `GET /api/ml/decision-boundary` | 결정 경계 시각화 | decisionBoundary.js |
| **ML** | `POST /api/ml/random-forest` | 랜덤 포레스트 | randomForest.js |
| **ML** | `POST /api/ml/kmeans` | K-Means 클러스터링 | kmeans.js |
| **ML** | `POST /api/ml/svm` | SVM 분류기 | svm.js |
| **ML** | `POST /api/ml/mlp` | 다층 퍼셉트론 | mlp.js |
| **ML** | `POST /api/ml/linear-regression` | 선형·다항 회귀 | linearRegression.js |
| **DL** | `POST /api/dl/cnn-timeseries` | CNN 시계열 예측 | cnnTimeseries.js |
| **DL** | `POST /api/dl/lstm-predictor` | LSTM 주가 예측 | lstm.js |
| **DL** | `POST /api/dl/transformer-timeseries` | Transformer 시계열 예측 | transformer.js |
| **NLP** | `POST /api/nlp/text-classify` | 텍스트 감성 분류 | textClassify.js · sentiment.js |
| **CV** | `POST /api/cv/circle-animation` | OpenCV 애니메이션 | opencv.js |

---

## 🐍 Python 라이브러리 구성 (`requirements.txt`)

| 카테고리 | 패키지 | 용도 |
|----------|--------|------|
| **웹 서버** | `fastapi`, `uvicorn`, `gunicorn` | REST API 서버 |
| **데이터 처리** | `numpy`, `pandas`, `scipy`, `statsmodels` | 수치 계산·통계 분석 |
| **금융 데이터** | `yfinance`, `pykrx` | 주가·재무 데이터 수집 |
| **기술적 분석** | `pandas-ta`, `mplfinance` | 130+ 기술 지표, 캔들 차트 |
| **시각화** | `matplotlib`, `seaborn`, `plotly` | 정적·인터랙티브 차트 |
| **리포트 생성** | `reportlab`, `openpyxl`, `pyarrow` | PDF·Excel·Parquet 출력 |
| **ML** | `scikit-learn` | 분류·회귀·클러스터링 |
| **딥러닝** | `torch`, `transformers`, `diffusers` | LSTM·Transformer·이미지 생성 |
| **컴퓨터 비전** | `opencv-python` | 영상 처리 |
| **유틸리티** | `requests`, `httpx`, `python-dotenv`, `orjson`, `aiofiles` | HTTP·환경변수·직렬화 |

---

## 💡 투자 분석 관련 핵심 영어 표현

| 표현 | 의미 |
|------|------|
| **Investment Analysis** | 투자 분석 |
| **Equity Research** | 주식 리서치 (증권사 리포트) |
| **Fundamental Analysis** | 기본적 분석 (내재가치 중심) |
| **Technical Analysis** | 기술적 분석 (차트·지표 중심) |
| **Quantitative Analysis** | 계량 분석 (통계·수학 모델) |
| **Valuation** | 가치 평가 (목표주가 산출) |
| **Due Diligence** | 투자 전 심층 실사 |
| **Peer Analysis** | 동종 기업 비교 분석 |
| **Buy / Hold / Sell** | 매수 / 보유 / 매도 의견 |
| **Outperform / Underperform** | 시장 수익률 상회 / 하회 |
| **Price Target** | 목표 주가 |
| **Bullish / Bearish** | 강세 / 약세 전망 |

> 📖 용어 사전: [docs/voca.md](docs/voca.md)

---

# 📌 DART API Key 발급 방법

DART(전자공시시스템) API는 상장 기업의 재무제표·공시 데이터를 무료로 수집할 수 있는 공공 API입니다.

### 발급 절차

| 단계 | 내용 |
|------|------|
| 1. 홈페이지 접속 | [https://opendart.fss.or.kr](https://opendart.fss.or.kr) |
| 2. 회원가입 | 오른쪽 상단 Login → 인증키 신청 → 이용약관 동의 |
| 3. 인증키 신청 | 상단 메뉴 **인증키 신청/관리 → 인증키 신청** |
| 4. 이메일 인증 | 신청 이메일로 발송된 인증 링크 클릭 |
| 5. 키 확인 | **인증키 신청/관리 → 오픈 API 이용현황** 에서 발급된 키 복사 |

> ⚠️ **유의사항**: 무료 제공 / 개인·기업 모두 발급 가능 / 하루 호출 횟수 제한 있음  
> 발급 후 프로젝트 루트의 `app/backend/.env` 파일에 `DART_API_KEY=발급받은키` 형식으로 입력

---

## 🗂️ Repository Structure

```text
.
├── app
│   ├── backend
│   │   ├── main.py                      # FastAPI 앱 & 전체 API 라우터
│   │   └── .env.example                 # 환경변수 템플릿 (DART_API_KEY 등)
│   ├── frontend
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── js
│   │       ├── app.js                   # SPA 라우터
│   │       ├── api.js                   # Fetch API 래퍼
│   │       └── views
│   │           ├── home.js
│   │           ├── macroRealtime.js     # 매크로 실시간 분석
│   │           ├── macroSimulation.js   # GBM 시뮬레이션
│   │           ├── industryAnalysis.js  # 산업 분석
│   │           ├── financialStatement.js # 재무제표
│   │           ├── dartCompanySearch.js  # DART 기업 검색
│   │           ├── valuation.js          # 밸류에이션
│   │           ├── technicalChart.js     # 기술적 분석 (7개 탭)
│   │           ├── backtest.js           # 백테스트
│   │           ├── portfolio.js          # 포트폴리오 최적화
│   │           ├── risk.js               # 리스크 분석
│   │           ├── pipeline.js           # 퀀트 파이프라인
│   │           ├── linearRegression.js   # ML: 선형 회귀
│   │           ├── decisionBoundary.js   # ML: 결정 경계
│   │           ├── randomForest.js       # ML: 랜덤 포레스트
│   │           ├── kmeans.js             # ML: K-Means
│   │           ├── svm.js                # ML: SVM
│   │           ├── mlp.js                # ML: MLP 신경망
│   │           ├── crossValidation.js    # ML: 교차검증
│   │           ├── cnnTimeseries.js      # DL: CNN 시계열
│   │           ├── lstm.js               # DL: LSTM 예측
│   │           ├── transformer.js        # DL: Transformer
│   │           ├── sentiment.js          # NLP: 감성 분석
│   │           ├── textClassify.js       # NLP: 텍스트 분류
│   │           ├── opencv.js             # CV: OpenCV
│   │           └── huggingface.js        # GenAI: 이미지 생성
│   └── src                              # 독립 실행 Python 스크립트
│       ├── QuantPipeline.py
│       ├── Backtest.py
│       ├── PortfolioOptimizer.py
│       ├── RiskManager.py
│       ├── CrossValid.py
│       ├── DecisionBoundary.py
│       ├── LinearRegression.py
│       ├── RandomForest.py
│       ├── KMeansClustering.py
│       ├── SVMClassifier.py
│       ├── NeuralNetMLP.py
│       ├── SentimentAnalysis.py
│       ├── OpenCVCPU.py
│       ├── HuggingFaceGPU.py
│       ├── CNNTimeSeries.py
│       ├── LSTMPredictor.py
│       └── TransformerTimeSeries.py
├── docs
│   ├── 27.md   Day 042 — 매크로 분석 개요 및 금리 분석
│   ├── 28.md   Day 043 — 경제지표 분석 (물가·유가 등)
│   ├── 29.md   Day 044 — 거시경제 상황 분석 실습
│   ├── 30.md   Day 045 — 산업 분석
│   ├── 31.md   Day 046 — 산업 분석 실습
│   ├── 32.md   Day 047 — 재무제표 분석 I
│   ├── 33.md   Day 048 — 재무제표 분석 II (현금흐름표 & 기업가치)
│   ├── 34.md   Day 049 — 상대가치 평가 (밸류에이션 멀티플)
│   ├── 35.md   Day 050 — 기술적 분석 I (추세 & 지표)
│   ├── 36.md   Day 051 — 기술적 분석 II + 통합 리포트
│   └── voca.md 투자분석 핵심 용어집
├── requirements.txt
└── readme.md
```

---

## 🚀 Quick Start

### 1) Python 앱 실행

#### /home/ubuntu/python-quant/app/backend/.env.example 를 .env 로 복제 후 본인 키 입력


```bash
cd /path/to/python-quant

python3 -m venv /home/ubuntu/python-quant/.venv && echo "venv created"
.venv/bin/pip install -r requirements.txt 2>&1

source /home/ubuntu/python-quant/.venv/bin/activate
cd app/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --env-file .env

```
---

```bash
pkill -f uvicorn

```

- 웹앱: `http://localhost:8000`
- API 문서: `http://localhost:8000/docs`
- 기본 헬스체크: `GET /api/health`


