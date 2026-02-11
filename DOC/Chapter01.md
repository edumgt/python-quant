# Chapter 01. 저장소 전체 지도와 학습 전략

이 저장소는 **기초 ML → 시각화 → 앙상블 → OpenCV → 생성형 AI** 흐름으로 설계되어 있습니다.

## 핵심 목표
- 코드 한 파일 단위로 실행 가능한 실습 경험 확보
- 모델 결과를 "숫자"와 "시각"으로 동시에 이해
- 로컬 스크립트를 API 서비스 형태로 확장하는 사고 훈련

## 권장 학습 순서
1. `CrossValid.py`
2. `DecisionBoundary.py`
3. `RandomForest.py`
4. `OpenCVCPU.py`
5. `HuggingFaceGPU.py`

## 이번 확장 포인트
- FastAPI 백엔드로 각 실습을 HTTP API로 제공
- Vanilla JS 프론트엔드 모듈로 실습 실행 UI 제공
- 클라우드 배포 시에도 동일한 흐름으로 재사용 가능
