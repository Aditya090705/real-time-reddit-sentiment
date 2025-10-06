// --- DOM Elements ---
const aiChartCanvas = document.getElementById('aiSentimentChart');
const emotionChartCanvas = document.getElementById('emotionChart');
const subredditSelect = document.getElementById('subredditSelect');
const updateBtn = document.getElementById('updateSubredditBtn');

// --- Initialize Charts ---
let aiChart = new Chart(aiChartCanvas.getContext('2d'), {
    type: 'doughnut',
    data: {
        labels: ['Positive','Negative','Neutral'],
        datasets: [{
            data: [
                parseInt(aiChartCanvas.dataset.positive),
                parseInt(aiChartCanvas.dataset.negative),
                parseInt(aiChartCanvas.dataset.neutral)
            ],
            backgroundColor: ['rgba(40,167,69,0.8)','rgba(220,53,69,0.8)','rgba(255,193,7,0.8)'],
            borderColor: '#fff',
            borderWidth: 2
        }]
    },
    options: { responsive: true, maintainAspectRatio: false }
});

let emotionChart = new Chart(emotionChartCanvas.getContext('2d'), {
    type: 'bar',
    data: {
        labels: ['Joy','Anger','Fear','Sadness','Love','Surprise'],
        datasets: [{
            label: 'Emotion Counts',
            data: [
                parseInt(emotionChartCanvas.dataset.joy),
                parseInt(emotionChartCanvas.dataset.anger),
                parseInt(emotionChartCanvas.dataset.fear),
                parseInt(emotionChartCanvas.dataset.sadness),
                parseInt(emotionChartCanvas.dataset.love),
                parseInt(emotionChartCanvas.dataset.surprise)
            ],
            backgroundColor: [
                'rgba(40,167,69,0.8)','rgba(220,53,69,0.8)',
                'rgba(128,0,128,0.8)','rgba(255,193,7,0.8)',
                'rgba(0,123,255,0.8)','rgba(255,105,180,0.8)'
            ],
            borderColor: '#fff',
            borderWidth: 1
        }]
    },
    options: { responsive: true, maintainAspectRatio: false }
});

// --- Update Dashboard Function ---
async function updateDashboard(subreddit) {
    try {
        const res = await fetch(`/fetch_posts?subreddit=${subreddit}`);
        const data = await res.json();

        // Update table
        const tbody = document.querySelector('tbody');
        tbody.innerHTML = '';
        data.posts.forEach(post => {
            const tr = document.createElement('tr');
            tr.className = post.ai_sentiment.toLowerCase();
            tr.innerHTML = `
                <td>${post.ai_sentiment}</td>
                <td>${post.ai_sentiment_score.toFixed(2)}</td>
                <td>${post.emotion}</td>
                <td>${post.emotion_score.toFixed(2)}</td>
                <td><a href="https://reddit.com${post.permalink}" target="_blank">${post.title}</a></td>
            `;
            tbody.appendChild(tr);
        });

        // Update charts
        aiChart.data.datasets[0].data = [data.ai_positive, data.ai_negative, data.ai_neutral];
        aiChart.update();

        emotionChart.data.datasets[0].data = [
            data.emotion_counts.joy,
            data.emotion_counts.anger,
            data.emotion_counts.fear,
            data.emotion_counts.sadness,
            data.emotion_counts.love,
            data.emotion_counts.surprise
        ];
        emotionChart.update();
    } catch (err) {
        console.error('Error updating dashboard:', err);
    }
}

// --- Event Listeners ---
updateBtn.addEventListener('click', () => {
    const subreddit = subredditSelect.value.trim() || 'technology';
    updateDashboard(subreddit);
});

// --- Predict Button Optimization ---
const predictBtn = document.getElementById('predictBtn');
predictBtn.addEventListener('click', async () => {
    const text = document.getElementById('userText').value;
    if (!text.trim()) return;

    const formData = new FormData();
    formData.append('text', text);

    const res = await fetch('/predict', { method: 'POST', body: formData });
    const data = await res.json();

    document.getElementById('predictionResult').innerHTML =
        `Sentiment: ${data.ai_sentiment} (${data.ai_sentiment_score})<br>
         Emotion: ${data.emotion} (${data.emotion_score})`;
});
