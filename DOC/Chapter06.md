# Chapter 06. HuggingFace Diffusers GPU 추론 이해

`HuggingFaceGPU.py`는 텍스트 프롬프트를 이미지로 변환하는 실습입니다.

## 필수 전제
- CUDA 지원 GPU
- `torch`, `diffusers` 설치
- 초기 모델 다운로드 네트워크

## 중요한 파라미터
- Prompt: 장면/스타일/구성 지시
- `guidance_scale`: 프롬프트 준수 강도
- `height`, `width`: 출력 해상도(높을수록 VRAM 요구 증가)

## API 설계 주의사항
- GPU 미존재 시 503 에러로 명확히 안내
- 생성 시간을 고려해 비동기 작업 큐로 확장 가능
