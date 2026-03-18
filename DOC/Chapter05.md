# Chapter 05. OpenCV로 영상 생성 흐름 이해 / Understanding OpenCV Video Generation

---

## 🇰🇷 한국어

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

## 🇺🇸 English

`OpenCVCPU.py` demonstrates the most fundamental pattern for building an MP4 from image frames.

### Frame-Based Thinking
- One image = one frame
- Combine frames in time order → video

### Code Highlights
- `VideoWriter`: specify codec, frame rate, and resolution
- `cv2.circle`: draw a circle on each frame
- Vary the radius in a loop to create animation

### API Benefits
- Dynamically generate videos from user input (width, height, FPS)
- Return the file as a URL so the browser can play it immediately

