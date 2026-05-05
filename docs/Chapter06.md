# Chapter 06. HuggingFace Diffusers GPU 추론 이해

> 💡 **쉽게 이해하기**: "빨간 장미가 있는 판타지 풍경화"처럼 텍스트를 입력하면 AI가 그림을 그려줍니다. GPU(CUDA)가 반드시 필요하며, HuggingFace `diffusers` 라이브러리로 Stable Diffusion 모델을 불러와 이미지를 생성합니다.

---

`HuggingFaceGPU.py`는 텍스트 프롬프트를 이미지로 변환하는 실습입니다.

### 필수 전제
- CUDA 지원 GPU
- `torch`, `diffusers` 설치
- 초기 모델 다운로드 네트워크

### 중요한 파라미터
- Prompt: 장면/스타일/구성 지시
- `guidance_scale`: 프롬프트 준수 강도
- `height`, `width`: 출력 해상도(높을수록 VRAM 요구 증가)

### API 설계 주의사항
- GPU 미존재 시 503 에러로 명확히 안내
- 생성 시간을 고려해 비동기 작업 큐로 확장 가능

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| Stable Diffusion 원리 | Computerphile | [Stable Diffusion - How does it work?](https://www.youtube.com/watch?v=1CIpzeNxIhU) |
| HuggingFace Diffusers | HuggingFace | [HuggingFace Diffusers Library](https://www.youtube.com/watch?v=J87hffSMB60) |
| PyTorch + GPU 기초 | freeCodeCamp | [PyTorch for Deep Learning - Full Course](https://www.youtube.com/watch?v=V_xro1bcAuA) |
