"""
Sentiment Analysis (NLP) Example
==================================
Uses TF-IDF + Logistic Regression to classify text sentiment.
Demonstrates a complete NLP pipeline using an inline corpus —
no internet download required.
Run standalone:
    python SentimentAnalysis.py
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

# ------------------------------------------------------------------
# 1. Inline bilingual training corpus — sports vs. politics
# ------------------------------------------------------------------
TEXTS = [
    # Sports (label 0)
    "The hockey team scored three goals in the final period to win the championship.",
    "Basketball playoffs begin next week with exciting matchups across the league.",
    "The pitcher threw a no-hitter in yesterday's baseball game.",
    "Football season kicks off with record-breaking ticket sales.",
    "The swimmer broke the world record in the 100m freestyle at the Olympics.",
    "Tennis star wins Grand Slam after coming back from injury.",
    "Ice hockey league announces expansion teams in new cities.",
    "The marathon runner finished in record time despite difficult conditions.",
    "Soccer World Cup qualifying matches start this weekend.",
    "Gold medals were awarded in gymnastics and rowing at the games.",
    "The team played amazing hockey tonight and won the Stanley Cup.",
    "Rookie quarterback leads the team to a stunning playoff victory.",
    # Politics (label 1)
    "The senator proposed a new budget policy for healthcare reform.",
    "Parliament voted on the controversial immigration bill last night.",
    "The president signed an executive order on environmental regulations.",
    "Political debates are heating up ahead of the upcoming election.",
    "The government announced a new economic stimulus package.",
    "Opposition leaders called for an emergency session of parliament.",
    "Tax reform legislation passed the Senate with bipartisan support.",
    "Foreign policy discussions dominated the United Nations summit.",
    "The prime minister addressed the nation about the economic crisis.",
    "Congressional hearings on data privacy began on Monday.",
    "Diplomatic talks between the two nations broke down over trade disputes.",
    "The government policy is controversial and misleading to the public.",
]
LABELS = [0] * 12 + [1] * 12
LABEL_NAMES = ["Sports", "Politics"]

# ------------------------------------------------------------------
# 2. Train / test split
# ------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(TEXTS, LABELS, test_size=0.25, random_state=42)

# ------------------------------------------------------------------
# 3. Pipeline: TF-IDF vectorizer + Logistic Regression
# ------------------------------------------------------------------
pipe = make_pipeline(
    TfidfVectorizer(max_features=500, ngram_range=(1, 2), stop_words="english"),
    LogisticRegression(max_iter=1000),
)
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

print(f"Classes: {LABEL_NAMES}")
print(f"Train: {len(X_train)}  Test: {len(X_test)}")
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=LABEL_NAMES))

# ------------------------------------------------------------------
# 4. Sample predictions
# ------------------------------------------------------------------
samples = [
    "Great goal! The team played amazing hockey tonight.",
    "The government policy is controversial and misleading.",
    "The Olympic swimmer set a new world record in the relay.",
    "Congress passed a bipartisan infrastructure bill.",
]
print("=== Sample Predictions ===")
for text in samples:
    pred = pipe.predict([text])[0]
    conf = pipe.predict_proba([text])[0][pred]
    print(f"[{LABEL_NAMES[pred]} {conf:.0%}] {text[:60]}…")

