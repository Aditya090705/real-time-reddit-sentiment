import praw
from ai_processing import enrich_post  # AI sentiment + emotion

# Reddit API credentials
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="RealTimeSentimentBot/0.1"
)
reddit.read_only = True

def fetch_posts(subreddit_name="technology", max_posts=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for post in subreddit.new(limit=max_posts):
        enriched_post = enrich_post(post)  # returns a dictionary with "emotions" list

        # Take the top emotion for dashboard display
        top_emotion = enriched_post["emotions"][0] if enriched_post["emotions"] else {"emotion": "neutral", "score": 0}

        # Prepare dictionary for dashboard
        posts.append({
            "title": post.title,
            "url": getattr(post, 'url', ''),  # existing link if needed
            "permalink": getattr(post, 'permalink', ''),  # THIS IS THE KEY
            "ai_sentiment": enriched_post["ai_sentiment"],
            "ai_sentiment_score": round(enriched_post["ai_sentiment_score"], 3),
            "emotion": top_emotion["emotion"],
            "emotion_score": round(top_emotion["score"], 3)
        })

    return posts
