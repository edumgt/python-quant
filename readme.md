<div align="center">

# 🐍 Python Quant Lab

**투자분석 기초부터 ML/DL 기반 퀀트 실습, FastAPI 서빙까지 한 번에 학습하는 실습형 저장소**

</div>

---

## 투자분석 기초 방법론

- 매크로 분석: 경제지표 분석(금리, 물가, 유가 등 주요 지표 보는 법), 거시경제상황 분석 실습

<img alt="투자분석 개요" src="image.png" />

- 산업 분석: 산업 경쟁력 분석(산업경쟁력 개념/분석모형, 산업별 분석방법), 산업 분석 실습
- 기본적 분석: 재무제표분석(손익계산서/대차대조표/현금흐름표), 기업가치분석(상대가치평가 밸류에이션(멀티플), 절대가치평가 밸류에이션(DCF, EVA, FCF 등)), 분석기업선정 및 밸류에이션 실습
- 기술적 분석: 추세 분석(지지선과 저항선, 이동평균선, 갭 반전, 되돌림 분석 등), 패턴 분석, 캔들 차트 분석, 지표 분석, 앨리어트파동이론, 분석기업선정 및 기술적 분석

---

## 저장소 구성에 맞춘 학습 맵

- **매크로 분석 실습**
  - 프론트: `app/frontend/js/views/macroRealtime.js`, `app/frontend/js/views/macroSimulation.js`
  - API: `/api/macro/realtime`, `/api/macro/simulation`
- **산업 분석 실습**
  - 프론트: `app/frontend/js/views/industryAnalysis.js`
  - API: `/api/industry/porter`, `/api/industry/sector`, `/api/industry/lifecycle`
- **기본적/퀀트 분석 실습**
  - 스크립트: `app/src/Backtest.py`, `app/src/PortfolioOptimizer.py`, `app/src/RiskManager.py`, `app/src/QuantPipeline.py`
  - API: `/api/quant/backtest`, `/api/quant/portfolio`, `/api/quant/risk`, `/api/quant/pipeline`
- **ML/DL 확장 실습**
  - 스크립트: `app/src/CrossValid.py`, `app/src/RandomForest.py`, `app/src/SVMClassifier.py`, `app/src/NeuralNetMLP.py`, `app/src/CNNTimeSeries.py`, `app/src/LSTMPredictor.py`, `app/src/TransformerTimeSeries.py`
  - API: `/api/ml/*`, `/api/dl/*`, `/api/nlp/text-classify`

---

## 🗂️ Repository Structure

```text
.
├── app
│   ├── backend
│   │   └── main.py
│   ├── frontend
│   │   ├── index.html
│   │   ├── styles.css
│   │   ├── package.json
│   │   └── js
│   │       ├── app.js
│   │       ├── api.js
│   │       └── views
│   └── src
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
│   └── 01.md ~ 80.md
├── requirements.txt
└── readme.md
```

---

## 🚀 Quick Start

### 1) Python API 서버 실행

```bash
cd /home/runner/work/python-quant/python-quant
pip install -r requirements.txt
uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload
```

- API 문서: `http://localhost:8000/docs`
- 기본 헬스체크: `GET /api/health`

### 2) 프론트엔드 실행

```bash
cd /home/runner/work/python-quant/python-quant/app/frontend
npm install
npm run dev
```

### 3) 대표 스크립트 실행

```bash
cd /home/runner/work/python-quant/python-quant
python app/src/QuantPipeline.py
python app/src/Backtest.py
python app/src/RiskManager.py
python app/src/PortfolioOptimizer.py
```

---

## 📘 문서

- `docs/01.md` ~ `docs/80.md`: 일차별 학습 문서

---

## 📄 License

MIT License
