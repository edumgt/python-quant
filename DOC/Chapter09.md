# Chapter 09. 클라우드 배포 시나리오

## 최소 배포 전략
1. Docker 이미지 빌드
2. Cloud Run/Render/Fly.io 등에 배포
3. 환경변수로 모델 ID, 리소스 제한 관리

## 권장 운영 옵션
- CPU 전용 인스턴스: ML/OpenCV 엔드포인트
- GPU 인스턴스: Diffusers 엔드포인트 분리 배포

## 운영 체크리스트
- CORS 정책
- 생성 파일 보관 정책(스토리지 오프로딩)
- 요청 제한(rate limiting)
- 로그/모니터링(응답 시간, 에러율)
