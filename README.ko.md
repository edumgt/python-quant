<div align="center">

# 🧠 Python ML/DL Education Lab

**Python FastAPI 백엔드 + Vanilla JS 프론트엔드로 구성한 ML/DL 교육 플랫폼**

[![GitHub Sponsors](https://img.shields.io/badge/후원하기-%E2%9D%A4-ea4aaa?logo=github-sponsors)](https://github.com/sponsors/edumgt)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📖 소개

이 저장소는 **기초 ML → 앙상블 → 클러스터링 → SVM → 신경망(MLP) → NLP → 컴퓨터 비전 → 생성형 AI** 순서로 구성된 파이썬 교육 플랫폼입니다.

각 실습 모듈은 두 가지 방식으로 실행 가능합니다:
- 🐍 **독립 Python 스크립트** — 간단히 `python KMeansClustering.py` 형태로 실행
- 🌐 **FastAPI REST API** — 브라우저 UI에서 파라미터를 조절하며 실행

---

## 🗂️ 디렉토리 구조

```text
.
├── CrossValid.py              # K-Fold 교차 검증
├── DecisionBoundary.py        # 결정 경계 시각화
├── RandomForest.py            # 랜덤 포레스트 분류기
├── KMeansClustering.py        # KMeans 비지도 클러스터링
├── SVMClassifier.py           # SVM 분류기 (RBF/Linear/Poly)
├── NeuralNetMLP.py            # MLP 신경망 분류기
├── LinearRegression.py        # 선형/다항 회귀
├── SentimentAnalysis.py       # TF-IDF + LR 텍스트 분류
├── HuggingFaceGPU.py          # Stable Diffusion (GPU)
├── requirements.txt
├── DOC/
│   ├── Chapter01.md ~ Chapter14.md
└── app/
    ├── backend/
    │   └── main.py            # FastAPI 서버 (모든 엔드포인트)
    └── frontend/
        ├── package.json       # Node.js 개발 환경
        ├── index.html
        ├── styles.css
        └── js/
            ├── app.js
            ├── api.js
            └── views/        # 실습별 UI 컴포넌트
```

---

## 🚀 실행 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. FastAPI 서버 실행

```bash
uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload
```

브라우저에서 `http://localhost:8000` 접속 후 각 실습 모듈을 실행할 수 있습니다.

### 3. Node.js 개발 서버 (선택)

```bash
cd app/frontend
npm install
npm run dev    # http://localhost:3000
```

### 4. 독립 스크립트 실행

```bash
python CrossValid.py           # 교차 검증
python DecisionBoundary.py     # 결정 경계 시각화
python RandomForest.py         # 랜덤 포레스트
python KMeansClustering.py     # KMeans 클러스터링
python SVMClassifier.py        # SVM 분류
python NeuralNetMLP.py         # MLP 신경망
python LinearRegression.py     # 회귀 분석
python SentimentAnalysis.py    # 텍스트 분류
```

---

## 📡 API 엔드포인트

| Method | 경로 | 설명 |
|--------|------|------|
| `GET`  | `/api/health` | 서버 상태 확인 |
| `POST` | `/api/ml/cross-validation` | K-Fold 교차 검증 |
| `GET`  | `/api/ml/decision-boundary` | 결정 경계 시각화 이미지 |
| `POST` | `/api/ml/random-forest` | 랜덤 포레스트 분류 결과 |
| `POST` | `/api/ml/kmeans` | KMeans 클러스터링 + Elbow 그래프 |
| `POST` | `/api/ml/svm` | SVM 분류 (커널 선택 가능) |
| `POST` | `/api/ml/mlp` | MLP 신경망 학습 및 손실 곡선 |
| `POST` | `/api/ml/linear-regression` | 선형/다항 회귀 |
| `POST` | `/api/nlp/text-classify` | TF-IDF 텍스트 분류 |
| `POST` | `/api/cv/circle-animation` | OpenCV 영상 생성 |
| `POST` | `/api/genai/text-to-image` | Stable Diffusion (GPU 필요) |

> 자동 생성 Swagger UI: `http://localhost:8000/docs`

---

## 📚 학습 커리큘럼

| 챕터 | 주제 | 스크립트 |
|------|------|---------|
| 01 | 저장소 구성 및 학습 전략 | — |
| 02 | Cross Validation 이해 | `CrossValid.py` |
| 03 | Decision Boundary 시각화 | `DecisionBoundary.py` |
| 04 | Random Forest 결과 해석 | `RandomForest.py` |
| 05 | OpenCV 영상 생성 | `OpenCVCPU.py` |
| 06 | HuggingFace Diffusers | `HuggingFaceGPU.py` |
| 07 | FastAPI 백엔드 구조 | `app/backend/main.py` |
| 08 | Vanilla JS 프론트엔드 모듈 | `app/frontend/` |
| 09 | 클라우드 배포 시나리오 | — |
| 10 | 실습 과제 목록 | — |
| 11 | KMeans 비지도 클러스터링 | `KMeansClustering.py` |
| 12 | SVM 분류기 | `SVMClassifier.py` |
| 13 | MLP 신경망 | `NeuralNetMLP.py` |
| 14 | NLP 텍스트 분류 | `SentimentAnalysis.py` |

---

## 💖 후원

이 프로젝트가 도움이 되셨다면 GitHub Sponsors로 후원해 주세요!

후원금은 다음에 사용됩니다:
- ✨ 새로운 ML/DL 예제 추가
- 📖 문서 품질 개선
- 🖥️ 클라우드 인프라 유지
- 🎓 교육 컨텐츠 확장

[![후원하기](https://img.shields.io/badge/GitHub%20Sponsors로%20후원하기-%E2%9D%A4-ea4aaa?logo=github-sponsors&style=for-the-badge)](https://github.com/sponsors/edumgt)

---

## 🤝 기여

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고해 PR을 보내주세요.

---

## 📄 라이선스

[MIT License](LICENSE) © edumgt
