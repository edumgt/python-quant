# Chapter 03. Decision Boundary 시각화 해설

> 💡 **쉽게 이해하기**: 빨간 공과 파란 공이 섞인 지도에서 두 그룹을 나누는 경계선을 그리는 것입니다. 모델이 공간을 어떻게 분류하는지 색깔 지도로 눈으로 직접 확인할 수 있어 머신러닝 개념 이해에 큰 도움이 됩니다.

---

`DecisionBoundary.py`는 모델이 공간을 어떻게 나누는지 시각적으로 보여줍니다.

### 핵심 개념
- 입력 특징이 2차원일 때, 모델은 평면 위의 경계를 학습
- 경계 한쪽은 클래스 0, 다른 쪽은 클래스 1로 예측

### 구현 흐름
1. 2차원 데이터 생성
2. 학습/검증 분리
3. 로지스틱 회귀 학습
4. `meshgrid`로 촘촘한 점 생성
5. 각 점 예측 결과를 색으로 렌더링

### API/클라우드 관점
- 서버에서 PNG를 생성해 base64로 전달
- 브라우저는 `<img>`로 즉시 표시
- 원격 환경에서도 `plt.show()` 없이 동일한 시각화 제공

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| Logistic Regression | StatQuest | [Logistic Regression, Clearly Explained](https://www.youtube.com/watch?v=yIYKR4sgzI8) |
| Decision Boundary 개념 | StatQuest | [Decision Trees, Part 1](https://www.youtube.com/watch?v=7VeUPuFGJHk) |
| matplotlib 시각화 | Corey Schafer | [Matplotlib Tutorial Series](https://www.youtube.com/watch?v=UO98lJQ3QGI) |
