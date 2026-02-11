# Chapter 07. FastAPI 백엔드 구조 설명

이번 구성에서는 `app/backend/main.py`에 학습용 엔드포인트를 통합했습니다.

## 엔드포인트 개요
- `POST /api/ml/cross-validation`
- `GET /api/ml/decision-boundary`
- `POST /api/ml/random-forest`
- `POST /api/cv/circle-animation`
- `POST /api/genai/text-to-image`

## 설계 포인트
- Pydantic 모델로 입력 검증
- 생성 산출물은 `app/generated/`에 저장
- 정적 파일/프론트엔드는 FastAPI에서 함께 서빙

## 배포 포인트
- `uvicorn app.backend.main:app --host 0.0.0.0 --port 8000`
- 단일 컨테이너에서 백엔드+프론트 통합 운영 가능
