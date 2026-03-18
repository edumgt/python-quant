# Chapter 14. NLP Text Classification — 텍스트 분류 / Text Classification

---

## 🇰🇷 한국어

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

## 🇺🇸 English

### Core Concept

The first step in NLP is converting text into numerical vectors.  
This module uses a **TF-IDF vectorizer → Logistic Regression** pipeline for text classification.

### What is TF-IDF?

- **TF (Term Frequency)**: How often a word appears in a document
- **IDF (Inverse Document Frequency)**: Higher weight for rare words across all documents
- Common words (the, is) → low score; distinctive words → high score

### Pipeline

```python
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ('clf',   LogisticRegression()),
])
```

1. `TfidfVectorizer`: text → sparse matrix (documents × vocabulary)
2. `ngram_range=(1,2)`: includes unigrams and bigrams
3. `LogisticRegression`: classifies sparse vectors

### Dataset

Two categories from 20 Newsgroups:
- `rec.sport.hockey` → Sports
- `talk.politics.misc` → Politics

### API Extension Points

- Classify user-input text in real time
- Display confidence alongside predicted label
- Easily extensible to more categories

### Further Directions

- Fine-tune a HuggingFace BERT model for higher accuracy
- Add multi-label classification for mixed-topic texts
- Integrate with a database to build a labeled dataset over time
