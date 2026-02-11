# Chapter 04. Random Forest 분류 결과 읽는 법

`RandomForest.py`는 트리 앙상블 기반의 대표 분류 모델을 다룹니다.

## 모델 이해
- 여러 의사결정트리의 다수결로 최종 클래스 결정
- 단일 트리보다 과적합에 강하고 성능이 안정적인 편

## 출력 지표
- Accuracy: 전체 정답 비율
- Precision/Recall/F1: 클래스별 성능 균형 확인

## 실무 확장 팁
- 가상 데이터 대신 CSV를 연결
- 범주형 인코딩, 결측치 처리 파이프라인 추가
- API 응답에 feature importance를 포함해 설명 가능성 강화
