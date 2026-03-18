<div align="center">

# 🧠 Python ML/DL Education Lab

**Python FastAPI 백엔드 + Vanilla JS 프론트엔드로 구성한 ML/DL 교육 플랫폼**

**ML/DL Education Platform with Python FastAPI Backend + Vanilla JS Frontend**

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-ea4aaa?logo=github-sponsors)](https://github.com/sponsors/edumgt)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[**한국어 README**](README.ko.md) | [**English README**](README.en.md) | [**📚 Docs**](DOC/)

</div>

---

## 📖 소개 / Introduction

이 저장소는 **기초 ML → 신경망 → NLP → 컴퓨터 비전 → 생성형 AI** 흐름으로 구성한 교육용 실습 플랫폼입니다.  
각 실습 모듈은 **독립 Python 스크립트**와 **FastAPI REST API** 두 가지 방식으로 실행할 수 있습니다.

This repository is an educational lab platform organized from **basic ML → neural networks → NLP → computer vision → generative AI**.  
Each module can be run as a **standalone Python script** or accessed via a **FastAPI REST API**.

---

## 🗂️ 구성 / Structure

```text
.
├── CrossValid.py              # K-Fold Cross Validation
├── DecisionBoundary.py        # Decision Boundary Visualization
├── RandomForest.py            # Random Forest Classifier
├── KMeansClustering.py        # KMeans Unsupervised Clustering  [NEW]
├── SVMClassifier.py           # SVM with RBF/Linear/Poly kernel  [NEW]
├── NeuralNetMLP.py            # MLP Neural Network               [NEW]
├── LinearRegression.py        # Linear & Polynomial Regression   [NEW]
├── SentimentAnalysis.py       # TF-IDF + LR Text Classification  [NEW]
├── HuggingFaceGPU.py          # Stable Diffusion (GPU)
├── requirements.txt
├── DOC/
│   ├── Chapter01.md ~ Chapter14.md   (한국어 + English)
└── app/
    ├── backend/
    │   └── main.py            # FastAPI server (all endpoints)
    └── frontend/
        ├── package.json       # Node.js dev setup
        ├── index.html
        ├── styles.css
        └── js/
            ├── app.js
            ├── api.js
            └── views/
                ├── home.js
                ├── crossValidation.js
                ├── decisionBoundary.js
                ├── randomForest.js
                ├── kmeans.js         [NEW]
                ├── svm.js            [NEW]
                ├── mlp.js            [NEW]
                ├── linearRegression.js [NEW]
                ├── sentiment.js      [NEW]
                ├── opencv.js
                └── huggingface.js
```

---

## 🚀 실행 방법 / Quick Start

### Python 환경 설정 / Python Setup

```bash
# 1. 의존성 설치 / Install dependencies
pip install -r requirements.txt

# 2. 서버 실행 / Start server
uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload

# 3. 브라우저 접속 / Open browser
# http://localhost:8000
```

### Node.js 개발 서버 / Node.js Dev Server

```bash
cd app/frontend
npm install       # devDependencies 설치
npm run dev       # http://localhost:3000 (CORS 포함)
```

### 독립 스크립트 실행 / Run Standalone Scripts

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

## 📡 API 엔드포인트 / API Endpoints

| Method | Endpoint | 설명 / Description |
|--------|----------|-------------------|
| `GET`  | `/api/health` | 서버 상태 확인 / Health check |
| `POST` | `/api/ml/cross-validation` | K-Fold 교차 검증 |
| `GET`  | `/api/ml/decision-boundary` | 결정 경계 시각화 |
| `POST` | `/api/ml/random-forest` | 랜덤 포레스트 분류 |
| `POST` | `/api/ml/kmeans` | KMeans 클러스터링 |
| `POST` | `/api/ml/svm` | SVM 분류 (커널 선택 가능) |
| `POST` | `/api/ml/mlp` | MLP 신경망 분류 |
| `POST` | `/api/ml/linear-regression` | 선형/다항 회귀 |
| `POST` | `/api/nlp/text-classify` | TF-IDF 텍스트 분류 |
| `POST` | `/api/cv/circle-animation` | OpenCV 영상 생성 |
| `POST` | `/api/genai/text-to-image` | Stable Diffusion (GPU 필요) |

전체 API 문서: `http://localhost:8000/docs` (Swagger UI 자동 생성)

Full API docs auto-generated at: `http://localhost:8000/docs`

---

## 📚 학습 커리큘럼 / Learning Curriculum

| Chapter | 주제 / Topic | 스크립트 / Script |
|---------|-------------|-----------------|
| 01 | 저장소 구성 및 학습 전략 / Repo overview | — |
| 02 | Cross Validation 이해 / Understanding CV | `CrossValid.py` |
| 03 | Decision Boundary 시각화 / Visualization | `DecisionBoundary.py` |
| 04 | Random Forest 결과 해석 / RF Results | `RandomForest.py` |
| 05 | OpenCV 영상 생성 / Video generation | `OpenCVCPU.py` |
| 06 | HuggingFace Diffusers / GenAI | `HuggingFaceGPU.py` |
| 07 | FastAPI 백엔드 구조 / BE structure | `app/backend/main.py` |
| 08 | Vanilla JS 프론트엔드 / FE modules | `app/frontend/` |
| 09 | 클라우드 배포 시나리오 / Cloud deploy | — |
| 10 | 실습 과제 / Practice tasks | — |
| 11 | KMeans Clustering | `KMeansClustering.py` |
| 12 | SVM Classifier | `SVMClassifier.py` |
| 13 | MLP Neural Network | `NeuralNetMLP.py` |
| 14 | NLP Text Classification | `SentimentAnalysis.py` |

---

## 💖 후원 / Sponsorship

이 프로젝트가 학습에 도움이 되었다면 GitHub Sponsor로 응원해 주세요!  
If this project helped your learning, please consider sponsoring via GitHub Sponsors!

[![Sponsor](https://img.shields.io/badge/Sponsor%20this%20project-%E2%9D%A4-ea4aaa?logo=github-sponsors&style=for-the-badge)](https://github.com/sponsors/edumgt)

후원금은 새로운 예제 추가, 문서 개선, 클라우드 인프라 유지에 사용됩니다.  
Sponsorship funds go toward new examples, documentation improvements, and cloud infrastructure.

---

## 🤝 기여 / Contributing

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고해 주세요. / Please see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 라이선스 / License

[MIT License](LICENSE) © edumgt

