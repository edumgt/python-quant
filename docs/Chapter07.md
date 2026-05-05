# Chapter 07. FastAPI 백엔드 구조 설명

> 💡 **쉽게 이해하기**: 로컬에서 실행하던 머신러닝 코드를 웹 API로 바꿔 누구나 인터넷으로 사용할 수 있게 만드는 과정입니다. FastAPI는 Python으로 API 서버를 빠르게 만드는 프레임워크이며, 각 머신러닝 기능이 하나의 엔드포인트(/api/ml/...)로 연결됩니다.

---

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

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| FastAPI 입문 | Tech With Tim | [FastAPI Tutorial - Building RESTful APIs](https://www.youtube.com/watch?v=7t2alSnE2-I) |
| Pydantic 데이터 검증 | ArjanCodes | [Pydantic Tutorial - Data Validation in Python](https://www.youtube.com/watch?v=Vj-iU-8_xLs) |
| Uvicorn / ASGI | ArjanCodes | [FastAPI Design Patterns](https://www.youtube.com/watch?v=oBDp0FCKQQQ) |
