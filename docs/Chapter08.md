# Chapter 08. Vanilla JS 프론트엔드 모듈 구성

> 💡 **쉽게 이해하기**: React나 Vue 같은 프레임워크 없이, 순수 자바스크립트(Vanilla JS)만으로 프론트엔드를 만든 구조입니다. 파일 역할이 명확히 분리되어 있어 배우기 쉽고, 백엔드 API를 브라우저에서 `fetch`로 바로 호출할 수 있습니다.

---

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

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| JavaScript 기초 | Traversy Media | [JavaScript Crash Course For Beginners](https://www.youtube.com/watch?v=hdI2bqOjy3c) |
| Fetch API / 비동기 | Traversy Media | [Fetch API Introduction](https://www.youtube.com/watch?v=Oive66jrwBs) |
| ES6 모듈 구조 | Fireship | [JavaScript Modules in 100 Seconds](https://www.youtube.com/watch?v=qgRUr-YUk1Q) |
| Node.js 개발환경 | The Net Ninja | [Node.js Crash Course](https://www.youtube.com/watch?v=zb3Qk8SG5Ms) |
