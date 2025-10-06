from flask import Flask, render_template, request, jsonify
from fetch_reddit import fetch_posts
from ai_processing import get_sentiment, get_emotions  # your AI functions

app = Flask(__name__)

# Homepage
@app.route('/')
def index():
    default_subreddit = "technology"
    posts = fetch_posts(subreddit_name=default_subreddit, max_posts=10)
    ai_positive, ai_negative, ai_neutral, emotion_counts = get_counts(posts)

    return render_template(
        "index.html",
        posts=posts,
        ai_positive=ai_positive,
        ai_negative=ai_negative,
        ai_neutral=ai_neutral,
        emotion_counts=emotion_counts,
        default_subreddit=default_subreddit
    )

# Predict user text sentiment
@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text', '')
    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    sentiment, sentiment_score = get_sentiment(text)
    emotions = get_emotions(text)
    top_emotion = emotions[0] if emotions else {"emotion": "neutral", "score": 0.0}

    return jsonify({
        "ai_sentiment": sentiment,
        "ai_sentiment_score": round(sentiment_score, 3),
        "emotion": top_emotion["emotion"],
        "emotion_score": round(top_emotion["score"], 3)
    })

# Fetch latest posts for a given subreddit (used by dropdown/update button)
@app.route('/fetch_posts', methods=['GET'])
def fetch_posts_api():
    subreddit_name = request.args.get('subreddit', 'technology')
    posts = fetch_posts(subreddit_name=subreddit_name, max_posts=10)
    ai_positive, ai_negative, ai_neutral, emotion_counts = get_counts(posts)

    return jsonify({
        "posts": posts,
        "ai_positive": ai_positive,
        "ai_negative": ai_negative,
        "ai_neutral": ai_neutral,
        "emotion_counts": emotion_counts
    })

def get_counts(posts):
    ai_positive = sum(1 for p in posts if p['ai_sentiment'] == "POSITIVE")
    ai_negative = sum(1 for p in posts if p['ai_sentiment'] == "NEGATIVE")
    ai_neutral = sum(1 for p in posts if p['ai_sentiment'] == "NEUTRAL")

    emotions_list = ["joy", "anger", "fear", "sadness", "love", "surprise"]
    emotion_counts = {e: 0 for e in emotions_list}
    for p in posts:
        emotion = p.get('emotion', '').lower()
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1

    return ai_positive, ai_negative, ai_neutral, emotion_counts

if __name__ == "__main__":
    app.run(debug=True)
