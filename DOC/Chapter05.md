# Chapter 05. OpenCV로 영상 생성 흐름 이해

> 💡 **쉽게 이해하기**: 플립북(flipbook) 애니메이션처럼, 이미지 한 장 한 장을 쌓아 동영상을 만드는 원리입니다. `VideoWriter`로 코덱·프레임레이트·해상도를 설정하고, 반복문으로 프레임을 추가하면 mp4가 완성됩니다.

---

`OpenCVCPU.py`는 이미지 프레임을 쌓아 mp4를 만드는 가장 기본 패턴입니다.

### 프레임 기반 사고
- 한 장의 이미지 = 한 프레임
- 프레임을 시간 순으로 합치면 비디오

### 코드 포인트
- `VideoWriter`: 코덱/프레임레이트/해상도 지정
- `cv2.circle`: 각 프레임에 원을 그림
- 반복문에서 반지름을 변화시켜 애니메이션 구현

### API화 이점
- 사용자 입력(너비, 높이, FPS)으로 동영상 동적 생성
- 생성 파일을 URL로 반환하여 브라우저에서 바로 재생

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| OpenCV Python 기초 | freeCodeCamp | [OpenCV Course - Full Tutorial with Python](https://www.youtube.com/watch?v=oXlwWbU8l2o) |
| VideoWriter / 영상 처리 | sentdex | [Python plays GTA V (OpenCV series)](https://www.youtube.com/watch?v=ks4MPfMq8aQ) |
| Computer Vision 입문 | MIT OpenCourseWare | [Computer Vision](https://www.youtube.com/watch?v=715uLCHt4jE) |
