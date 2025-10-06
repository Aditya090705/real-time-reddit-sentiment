from transformers import pipeline

# --- Initialize models ---
# Fast & accurate sentiment analysis
sentiment_model = pipeline(
    "sentiment-analysis",
    model="siebert/sentiment-roberta-large-english",  # fast & robust
    device=-1  # CPU
)

# Emotion analysis
emotion_model = pipeline(
    "text-classification",
    model="nateraw/bert-base-uncased-emotion",
    top_k=None,  # return all emotions
    device=-1  # CPU
)

# Optional mapping: align sentiment to relevant emotions
SENTIMENT_EMOTION_MAP = {
    "POSITIVE": ["joy", "love", "surprise"],
    "NEGATIVE": ["anger", "fear", "sadness"],
    "NEUTRAL": ["surprise", "joy", "sadness"]
}


def get_sentiment(text):
    """
    Return sentiment label (POSITIVE/NEGATIVE/NEUTRAL) and confidence score.
    Low-confidence predictions are considered NEUTRAL.
    """
    result = sentiment_model(text[:512])[0]  # truncate text to 512 tokens
    label = result['label'].upper()          # POSITIVE / NEGATIVE
    score = result['score']

    # Threshold for Neutral sentiment
    if score < 0.7:
        label = "NEUTRAL"

    return label, round(score, 3)


def get_emotions(text, sentiment=None):
    """
    Return top 2 emotions (as a list of dicts) aligned with sentiment.
    Each dict: {"emotion": str, "score": float}
    """
    predictions = emotion_model(text[:512])[0]

    # Optional: filter emotions based on sentiment
    if sentiment and sentiment in SENTIMENT_EMOTION_MAP:
        allowed = [e.lower() for e in SENTIMENT_EMOTION_MAP[sentiment]]
        filtered = [p for p in predictions if p['label'].lower() in allowed]
    else:
        filtered = predictions

    # Fallback if no allowed emotions remain
    if not filtered:
        filtered = predictions

    # Sort by score descending
    filtered.sort(key=lambda x: x['score'], reverse=True)

    # Take top 2
    top_emotions = filtered[:2]

    return [{"emotion": e['label'].lower(), "score": round(e['score'], 3)} for e in top_emotions]


def enrich_post(post):
    """
    Enrich a Reddit post with AI sentiment and top emotions.
    Returns a dictionary:
    {
        "title": str,
        "url": str,
        "ai_sentiment": str,
        "ai_sentiment_score": float,
        "emotions": [{"emotion": str, "score": float}, ...]
    }
    """
    text = f"{post.title or ''} {getattr(post, 'selftext', '')}".strip()
    sentiment, sentiment_score = get_sentiment(text)
    emotions = get_emotions(text, sentiment)

    return {
        "title": post.title,
        "url": getattr(post, 'url', ''),
        "ai_sentiment": sentiment,
        "ai_sentiment_score": sentiment_score,
        "emotions": emotions
    }
