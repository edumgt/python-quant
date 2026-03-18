# Chapter 07. FastAPI 백엔드 구조 설명 / FastAPI Backend Structure

---

## 🇰🇷 한국어

이번 구성에서는 `app/backend/main.py`에 학습용 엔드포인트를 통합했습니다.

### 엔드포인트 개요

- `POST /api/ml/cross-validation`
- `GET /api/ml/decision-boundary`
- `POST /api/ml/random-forest`
- `POST /api/ml/kmeans`
- `POST /api/ml/svm`
- `POST /api/ml/mlp`
- `POST /api/ml/linear-regression`
- `POST /api/nlp/text-classify`
- `POST /api/cv/circle-animation`
- `POST /api/genai/text-to-image`

### 설계 포인트

- Pydantic 모델로 입력 검증
- 생성 산출물은 `app/generated/`에 저장
- 정적 파일/프론트엔드는 FastAPI에서 함께 서빙

### 배포 포인트

- `uvicorn app.backend.main:app --host 0.0.0.0 --port 8000`
- 단일 컨테이너에서 백엔드+프론트 통합 운영 가능

---

## 🇺🇸 English

All educational endpoints are consolidated in `app/backend/main.py`.

### Endpoint Overview

- `POST /api/ml/cross-validation`
- `GET /api/ml/decision-boundary`
- `POST /api/ml/random-forest`
- `POST /api/ml/kmeans`
- `POST /api/ml/svm`
- `POST /api/ml/mlp`
- `POST /api/ml/linear-regression`
- `POST /api/nlp/text-classify`
- `POST /api/cv/circle-animation`
- `POST /api/genai/text-to-image`

### Design Points

- Pydantic models for input validation with sensible defaults
- Generated artifacts stored in `app/generated/`
- Frontend static files served directly by FastAPI

### Deployment

- `uvicorn app.backend.main:app --host 0.0.0.0 --port 8000`
- Single container can serve both backend and frontend

