# Real-Time Reddit Sentiment

**Real-Time Reddit Sentiment** is an AI-powered dashboard that fetches live posts from Reddit, performs sentiment and emotion analysis using NLP, and visualizes the results in real time. This project helps users monitor public opinions, trends, and moods from social media dynamically.

---

## Features

- **Real-Time Reddit Data:** Fetches latest posts from any subreddit.
- **AI & NLP Sentiment Analysis:** Classifies posts into Positive, Negative, or Neutral.
- **Emotion Detection:** Identifies primary emotions like Joy, Anger, Fear, Sadness, Love, and Surprise.
- **Interactive Dashboard:**
  - Doughnut chart for sentiment distribution.
  - Bar chart for emotion distribution.
  - Table with post titles, AI sentiment, and emotion scores.
- **Custom Subreddit Selection:** Users can select which subreddit to monitor.
- **Text Prediction:** Users can input any text to predict sentiment and emotions instantly.
- **Auto Refresh:** Dashboard updates every 20 seconds for real-time monitoring.
- **Optimized Performance:** Fast updates even with large data and text inputs.

---

## Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript, Chart.js  
- **AI & NLP:** Custom sentiment & emotion analysis (using Python NLP libraries)  
- **API:** Reddit API via PRAW
  
---

## Usage

- Select a subreddit from the dropdown (e.g., `technology`, `sports`, `gaming`).  
- Click **Update** to fetch latest posts.  
- View AI sentiment, emotion analysis, and charts updating in real time.  
- Use the **Predict** feature to analyze custom text instantly.  

---

## Folder Structure

```plaintext
real-time-reddit-sentiment/
│
├── app.py                 # Main Flask application
├── fetch_reddit.py        # Reddit fetching logic
├── ai_processing.py       # Sentiment & emotion functions
├── templates/
│   └── index.html         # Dashboard frontend
├── static/
│   ├── style.css          # CSS
│   ├── chart.js           # Chart & auto-refresh JS
│   └── text_predict.js    # Text prediction JS
