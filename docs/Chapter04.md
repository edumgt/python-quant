# Chapter 04. Random Forest 분류 결과 읽는 법

> 💡 **쉽게 이해하기**: 전문가 한 명의 의견보다 전문가 100명의 다수결이 더 믿을 만합니다. 랜덤 포레스트는 수백 개의 결정 트리가 각자 예측하고 다수결로 최종 답을 내는 앙상블 모델입니다. 단일 트리보다 훨씬 안정적이고 과적합에 강합니다.

---

`RandomForest.py`는 트리 앙상블 기반의 대표 분류 모델을 다룹니다.

### 모델 이해
- 여러 의사결정트리의 다수결로 최종 클래스 결정
- 단일 트리보다 과적합에 강하고 성능이 안정적인 편

### 출력 지표
- Accuracy: 전체 정답 비율
- Precision/Recall/F1: 클래스별 성능 균형 확인

### 실무 확장 팁
- 가상 데이터 대신 CSV를 연결
- 범주형 인코딩, 결측치 처리 파이프라인 추가
- API 응답에 feature importance를 포함해 설명 가능성 강화

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| Decision Trees | StatQuest | [Decision Trees, Part 1](https://www.youtube.com/watch?v=7VeUPuFGJHk) |
| Random Forest | StatQuest | [Random Forests Part 1 - Building, Using and Evaluating](https://www.youtube.com/watch?v=J4Wdy0Wc_xQ) |
| Feature Importance | StatQuest | [Random Forests Part 2 - Missing Data and Clustering](https://www.youtube.com/watch?v=sQ870aTKqiM) |
