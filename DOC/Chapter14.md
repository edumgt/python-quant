# Chapter 14. NLP Text Classification — 텍스트 분류

> 💡 **쉽게 이해하기**: 텍스트를 숫자로 변환(TF-IDF)한 후 어떤 주제인지 분류하는 NLP의 기본 파이프라인입니다. "이 기사는 스포츠 기사인가, 정치 기사인가?"처럼 텍스트의 주제를 자동으로 분류할 수 있습니다.

---

### 핵심 개념

자연어 처리(NLP)의 첫 단계는 텍스트를 숫자 벡터로 변환하는 것입니다.  
이 실습에서는 **TF-IDF 벡터화 → 로지스틱 회귀** 파이프라인으로 텍스트를 분류합니다.

### TF-IDF란?

- **TF(Term Frequency)**: 한 문서 내 단어 빈도
- **IDF(Inverse Document Frequency)**: 전체 문서에서 희귀할수록 높은 가중치
- 흔한 단어(the, is)는 낮은 점수, 특징적인 단어는 높은 점수

### 파이프라인

```python
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ('clf',   LogisticRegression()),
])
```

1. `TfidfVectorizer`: 텍스트 → 희소 행렬 (문서 × 단어 수)
2. `ngram_range=(1,2)`: 단어 + 2-gram 패턴 포함
3. `LogisticRegression`: 희소 벡터 분류

### 데이터셋

20 Newsgroups 중 2개 카테고리 사용:
- `rec.sport.hockey` → 스포츠
- `talk.politics.misc` → 정치

### API 확장 포인트

- 사용자가 직접 입력한 텍스트를 실시간 분류
- 신뢰도(confidence)와 함께 결과 표시
- 더 많은 카테고리로 확장 가능

---

## 📺 참고 유튜브 영상

| 기술 스택 | 채널 | 링크 |
|---------|------|------|
| TF-IDF 개념 | StatQuest | [TF-IDF (Term Frequency - Inverse Document Frequency)](https://www.youtube.com/watch?v=OkFdqqyI8y4) |
| scikit-learn Pipeline | Data School | [Building a Machine Learning Pipeline](https://www.youtube.com/watch?v=irHhDMbw3xo) |
| BERT 입문 | HuggingFace | [Fine-tuning BERT for Text Classification](https://www.youtube.com/watch?v=GSt00_-0ncQ) |
| NLP 기초 개념 | StatQuest | [Word Embedding and Word2Vec, Clearly Explained](https://www.youtube.com/watch?v=viZrOnJclY0) |
