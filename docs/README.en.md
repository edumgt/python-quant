<div align="center">

# 🧠 Python ML/DL Education Lab

**An ML/DL Education Platform with Python FastAPI Backend + Vanilla JS Frontend**

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa?logo=github-sponsors)](https://github.com/sponsors/edumgt)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📖 Overview

This repository is a hands-on educational platform covering **basic ML → ensembles → clustering → SVM → neural networks (MLP) → NLP → computer vision → generative AI**.

Each module can be used in two ways:
- 🐍 **Standalone Python script** — simply run `python KMeansClustering.py`
- 🌐 **FastAPI REST API** — interact via the browser UI with adjustable parameters

---

## 🗂️ Directory Structure

```text
.
├── CrossValid.py              # K-Fold Cross Validation
├── DecisionBoundary.py        # Decision Boundary Visualization
├── RandomForest.py            # Random Forest Classifier
├── KMeansClustering.py        # KMeans Unsupervised Clustering
├── SVMClassifier.py           # SVM (RBF / Linear / Poly kernel)
├── NeuralNetMLP.py            # MLP Neural Network Classifier
├── LinearRegression.py        # Linear & Polynomial Regression
├── SentimentAnalysis.py       # TF-IDF + LR Text Classification
├── HuggingFaceGPU.py          # Stable Diffusion (GPU required)
├── requirements.txt
├── DOC/
│   ├── Chapter01.md ~ Chapter14.md   (Korean + English)
└── app/
    ├── backend/
    │   └── main.py            # FastAPI server (all endpoints)
    └── frontend/
        ├── package.json       # Node.js dev tooling
        ├── index.html
        ├── styles.css
        └── js/
            ├── app.js
            ├── api.js
            └── views/        # Per-module UI components
```

---

## 🚀 Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI server

```bash
uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000` to access the interactive dashboard.

### 3. Node.js dev server (optional)

```bash
cd app/frontend
npm install
npm run dev    # serves at http://localhost:3000 with CORS
```

### 4. Run standalone scripts

```bash
python CrossValid.py
python DecisionBoundary.py
python RandomForest.py
python KMeansClustering.py
python SVMClassifier.py
python NeuralNetMLP.py
python LinearRegression.py
python SentimentAnalysis.py
```

---

## 📡 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/api/health` | Server health check |
| `POST` | `/api/ml/cross-validation` | K-Fold cross-validation |
| `GET`  | `/api/ml/decision-boundary` | Decision boundary image |
| `POST` | `/api/ml/random-forest` | Random Forest classification |
| `POST` | `/api/ml/kmeans` | KMeans clustering + elbow plot |
| `POST` | `/api/ml/svm` | SVM (kernel selectable) |
| `POST` | `/api/ml/mlp` | MLP training + loss curve |
| `POST` | `/api/ml/linear-regression` | Linear / polynomial regression |
| `POST` | `/api/nlp/text-classify` | TF-IDF text classification |
| `POST` | `/api/cv/circle-animation` | OpenCV video generation |
| `POST` | `/api/genai/text-to-image` | Stable Diffusion (GPU required) |

> Auto-generated Swagger UI: `http://localhost:8000/docs`

---

## 📚 Learning Curriculum

| Chapter | Topic | Script |
|---------|-------|--------|
| 01 | Repository overview & learning strategy | — |
| 02 | Cross-Validation fundamentals | `CrossValid.py` |
| 03 | Decision Boundary visualization | `DecisionBoundary.py` |
| 04 | Random Forest result interpretation | `RandomForest.py` |
| 05 | OpenCV video generation | `OpenCVCPU.py` |
| 06 | HuggingFace Diffusers (GenAI) | `HuggingFaceGPU.py` |
| 07 | FastAPI backend structure | `app/backend/main.py` |
| 08 | Vanilla JS frontend modules | `app/frontend/` |
| 09 | Cloud deployment scenarios | — |
| 10 | Practice tasks | — |
| 11 | KMeans unsupervised clustering | `KMeansClustering.py` |
| 12 | SVM classifier | `SVMClassifier.py` |
| 13 | MLP neural network | `NeuralNetMLP.py` |
| 14 | NLP text classification | `SentimentAnalysis.py` |

---

## 💖 Sponsorship

If this project helped your learning, please consider sponsoring!

Your sponsorship funds:
- ✨ New ML/DL example modules
- 📖 Documentation improvements
- 🖥️ Cloud infrastructure
- 🎓 Educational content expansion

[![Sponsor this project](https://img.shields.io/badge/Sponsor%20this%20project-%E2%9D%A4-ea4aaa?logo=github-sponsors&style=for-the-badge)](https://github.com/sponsors/edumgt)

---

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a PR.

---

## 📄 License

[MIT License](LICENSE) © edumgt
