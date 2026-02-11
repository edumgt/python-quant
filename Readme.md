# Python & ML Education Repo

이 저장소는 Python 기반 ML/비전/생성형 AI 예제를 **클라우드 서빙 가능한 형태(FastAPI + Vanilla JS FE)**로 확장한 교육 프로젝트입니다.

## 구성

```text
.
├── CrossValid.py
├── DecisionBoundary.py
├── RandomForest.py
├── OpenCVCPU.py
├── HuggingFaceGPU.py
├── DOC/
│   ├── Chapter01.md
│   ├── ...
│   └── Chapter10.md
└── app/
    ├── backend/
    │   └── main.py
    ├── frontend/
    │   ├── index.html
    │   ├── styles.css
    │   └── js/
    │       ├── app.js
    │       ├── api.js
    │       └── views/
    └── generated/
```

## 실행 방법

```bash
pip install -r requirements.txt
uvicorn app.backend.main:app --host 0.0.0.0 --port 8000
```

브라우저에서 `http://localhost:8000` 접속 후 각 실습 모듈을 실행할 수 있습니다.

## API 요약

- `POST /api/ml/cross-validation`
- `GET /api/ml/decision-boundary`
- `POST /api/ml/random-forest`
- `POST /api/cv/circle-animation`
- `POST /api/genai/text-to-image`

## 문서

`DOC/Chapter01.md` ~ `DOC/Chapter10.md`에 예제 개념, API 확장, 클라우드 배포 전략을 순차적으로 정리했습니다.
