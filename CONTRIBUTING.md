# Contributing / 기여 가이드

[English](#english) | [한국어](#한국어)

---

## English

Thank you for considering a contribution to **Python ML/DL Education Lab**!

### Ways to Contribute

- 🐛 **Bug reports** — Open an issue describing the problem and how to reproduce it
- 💡 **Feature requests** — Suggest new ML/DL examples or UI improvements
- 📖 **Documentation** — Fix typos, improve explanations, add translations
- 🔧 **Code** — Implement new examples, fix bugs, improve tests

### Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/<your-username>/Python-ML-DL-Serving-Class.git
cd Python-ML-DL-Serving-Class

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Start the dev server
uvicorn app.backend.main:app --reload
```

### Adding a New ML/DL Module

1. **Create a standalone script** at the repository root (e.g., `MyNewModel.py`)
   - Include a docstring explaining what the script does
   - Use `matplotlib.use("Agg")` so it works without a display
   - Save output images/videos to a local file

2. **Add a backend endpoint** in `app/backend/main.py`
   - Define a Pydantic request model with sensible defaults and validation
   - Return a JSON response (include `image_base64` for plot outputs)

3. **Add a frontend view** in `app/frontend/js/views/<moduleName>.js`
   - Export a function `<moduleName>View(container)`
   - Use `withLoading`, `renderMetrics`, `renderImage`, `renderError` from `../api.js`

4. **Register the view** in `app/frontend/js/app.js`

5. **Add documentation** in `DOC/Chapter<NN>.md` in both Korean and English

### Code Style

- Python: follow [PEP 8](https://peps.python.org/pep-0008/); use type hints
- JavaScript: ES modules (`import`/`export`); no framework dependencies
- Keep functions small and focused (single responsibility)

### Pull Request Checklist

- [ ] New script runs standalone without errors
- [ ] New API endpoint returns consistent JSON structure
- [ ] Frontend view handles loading and error states
- [ ] Documentation chapter added/updated
- [ ] Existing functionality is not broken

---

## 한국어

**Python ML/DL Education Lab**에 기여해 주셔서 감사합니다!

### 기여 방법

- 🐛 **버그 신고** — 문제와 재현 방법을 이슈로 작성해 주세요
- 💡 **기능 제안** — 새 ML/DL 예제나 UI 개선 아이디어를 제안해 주세요
- 📖 **문서** — 오탈자 수정, 설명 개선, 번역 추가
- 🔧 **코드** — 새 예제 구현, 버그 수정, 테스트 개선

### 개발 환경 설정

```bash
# 1. 저장소 포크 후 클론
git clone https://github.com/<your-username>/Python-ML-DL-Serving-Class.git
cd Python-ML-DL-Serving-Class

# 2. Python 의존성 설치
pip install -r requirements.txt

# 3. 개발 서버 시작
uvicorn app.backend.main:app --reload
```

### 새 ML/DL 모듈 추가 방법

1. **루트에 독립 스크립트 생성** (예: `MyNewModel.py`)
   - 스크립트 상단에 목적을 설명하는 독스트링 포함
   - 디스플레이 없이 실행되도록 `matplotlib.use("Agg")` 사용
   - 출력 이미지/비디오를 로컬 파일로 저장

2. **`app/backend/main.py`에 엔드포인트 추가**
   - 합리적인 기본값과 검증 로직을 가진 Pydantic 요청 모델 정의
   - JSON 응답 반환 (플롯 출력 시 `image_base64` 포함)

3. **`app/frontend/js/views/<moduleName>.js`에 프론트엔드 뷰 추가**
   - `<moduleName>View(container)` 함수 내보내기
   - `../api.js`의 `withLoading`, `renderMetrics`, `renderImage`, `renderError` 활용

4. **`app/frontend/js/app.js`에 뷰 등록**

5. **`DOC/Chapter<NN>.md`에 한국어 + 영문 문서 추가**

### 코드 스타일

- Python: [PEP 8](https://peps.python.org/pep-0008/) 준수, 타입 힌트 사용
- JavaScript: ES 모듈(`import`/`export`) 사용, 프레임워크 의존성 없음
- 함수는 단일 책임 원칙에 따라 작게 유지

### PR 체크리스트

- [ ] 새 스크립트가 오류 없이 독립 실행됨
- [ ] 새 API 엔드포인트가 일관된 JSON 구조 반환
- [ ] 프론트엔드 뷰가 로딩 및 오류 상태 처리
- [ ] 문서 챕터 추가/업데이트
- [ ] 기존 기능 정상 동작 확인
