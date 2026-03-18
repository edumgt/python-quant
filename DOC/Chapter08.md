# Chapter 08. Vanilla JS 프론트엔드 모듈 구성 / Vanilla JS Frontend Module Structure

---

## 🇰🇷 한국어

프론트엔드는 프레임워크 없이 모듈 분리 방식으로 작성했습니다.

### 파일 구조
- `js/app.js`: 라우팅/메뉴
- `js/api.js`: fetch 래퍼 + 공통 헬퍼 (`withLoading`, `renderMetrics`, `renderImage`, `renderError`)
- `js/views/*.js`: 실습별 UI/이벤트

### 장점
- 번들러 없이도 빠르게 학습 가능
- API 호출과 화면 로직의 책임 분리
- 새로운 실습 추가 시 `views` 파일만 확장하면 됨

### Node.js 개발 환경

```bash
cd app/frontend
npm install
npm run dev   # http://localhost:3000
```

---

## 🇺🇸 English

The frontend is written with module separation and no framework dependencies.

### File Structure
- `js/app.js`: routing and navigation menu
- `js/api.js`: fetch wrappers + shared helpers (`withLoading`, `renderMetrics`, `renderImage`, `renderError`)
- `js/views/*.js`: per-module UI and event logic

### Advantages
- Learn quickly without a bundler
- Clean separation between API calls and rendering logic
- Add a new module by simply creating a new file in `views/`

### Node.js Dev Setup

```bash
cd app/frontend
npm install
npm run dev   # http://localhost:3000
```

