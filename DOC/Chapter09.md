# Chapter 09. 클라우드 배포 시나리오

> 💡 **쉽게 이해하기**: 내 PC에서만 돌던 서버를 인터넷 어디서든 접속할 수 있게 클라우드에 배포하는 방법입니다. Docker로 애플리케이션을 박스(컨테이너)에 담으면 어떤 서버 환경에서도 동일하게 실행됩니다.

---

### 최소 배포 전략
1. Docker 이미지 빌드
2. Cloud Run/Render/Fly.io 등에 배포
3. 환경변수로 모델 ID, 리소스 제한 관리

### 권장 운영 옵션
- CPU 전용 인스턴스: ML/OpenCV 엔드포인트
- GPU 인스턴스: Diffusers 엔드포인트 분리 배포

### 운영 체크리스트
- CORS 정책
- 생성 파일 보관 정책(스토리지 오프로딩)
- 요청 제한(rate limiting)
- 로그/모니터링(응답 시간, 에러율)

### Dockerfile 예시

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| Docker 입문 | TechWorld with Nana | [Docker Tutorial for Beginners](https://www.youtube.com/watch?v=3c-iBn73dDE) |
| Dockerfile 작성법 | Fireship | [Docker in 100 Seconds](https://www.youtube.com/watch?v=Gjnup-PuquQ) |
| Cloud Run 배포 | Google Cloud | [Cloud Run Quickstart](https://www.youtube.com/watch?v=1t_2bxf4RwI) |
| Fly.io 배포 | Traversy Media | [Deploy Apps with Fly.io](https://www.youtube.com/watch?v=J9GQaDXu5TQ) |
