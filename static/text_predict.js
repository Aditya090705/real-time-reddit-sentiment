document.getElementById("predictBtn").addEventListener("click", async () => {
    const text = document.getElementById("userText").value;
    if (!text.trim()) return alert("Please enter some text.");

    const formData = new FormData();
    formData.append("text", text);

    const response = await fetch("/predict", {
        method: "POST",
        body: formData
    });

    const resultDiv = document.getElementById("predictionResult");

    if (response.ok) {
        const data = await response.json();
        resultDiv.innerHTML = `
            AI Sentiment: <strong>${data.ai_sentiment}</strong> (${data.ai_sentiment_score})<br>
            Emotion: <strong>${data.emotion}</strong> (${data.emotion_score})
        `;
    } else {
        const err = await response.json();
        resultDiv.innerHTML = `<span style="color:red;">Error: ${err.error}</span>`;
    }
});
