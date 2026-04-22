# 🚀 Cold Email Success Predictor

Professional Machine Learning-driven outreach intelligence system. Analyze your cold emails for success probability, linguistic clarity, personalization, and tone before sending.

## 🌟 Key Features

*   **AI Success Scoring**: Real-time probability prediction (0-100%) using Logistic Regression & TF-IDF.
*   **Metric Breakdown**: Granular scores for Personalization, Clarity, Relevance, Tone, and Length.
*   **Actionable Suggestions**: Specific feedback on how to improve your email's engagement.
*   **Linguistic Insights**: Automated detection of word counts, tone categories, and personalization triggers.
*   **Production Dashboard**: High-fidelity glassmorphism UI with real-time API health monitoring.
*   **Full Deployment Support**: Architecture designed for Render (Backend) and InfinityFree (Frontend).

## 🛠️ Tech Stack

*   **Backend**: Python 3.x, FastAPI, Uvicorn
*   **Machine Learning**: Scikit-Learn (Logistic Regression), Pandas, NumPy
*   **Frontend**: PHP 8.x (XAMPP/Apache), Vanilla CSS (Outfit Typography), JavaScript (Fetch API)
*   **DevOps**: REST API Architecture, CORS Middleware, Health Check Monitoring

## 📂 Project Structure

```text
dell_ai_project/
├── backend/                # Python API & ML Logic
│   ├── app.py              # FastAPI Main Entry
│   ├── utils.py            # Feature Extraction & Analysis logic
│   ├── train_model.py      # ML Training Pipeline
│   ├── generate_dataset.py # Synthetic Data Generation
│   ├── model.pkl           # Trained LR Model
│   ├── vectorizer.pkl      # TF-IDF Vectorizer
│   └── requirements.txt    # Python Dependencies
├── frontend/               # Web Application
│   ├── index.php           # Main Interface Logic
│   └── styles.css          # Premium Styling
└── README.md               # Documentation
```

## 🚀 Local Setup Instructions

### 1. Backend Setup
1.  Navigate to the `backend/` directory.
2.  (Optional) Create a virtual environment: `python -m venv venv`.
3.  Install dependencies: `pip install -r requirements.txt`.
4.  Retrain the model (if needed): `python train_model.py`.
5.  Start the FastAPI server: `uvicorn app:app --host 0.0.0.0 --port 10000`.
    *   *Verify at:* `http://localhost:10000/health`

### 2. Frontend Setup
1.  Ensure you have **XAMPP** or a local LAMP/WAMP server running.
2.  Place the `dell_ai_project` folder in your `htdocs` directory.
3.  Open your browser and navigate to: `http://coldemail.page.gd/?i=1`.

## ☁️ Deployment Guide

### A. Backend (Render)
1.  Create a new **Web Service** on Render.
2.  Connect your GitHub repository.
3.  **Environment**: `Python 3`.
4.  **Build Command**: `pip install -r requirements.txt`.
5.  **Start Command**: `uvicorn app:app --host 0.0.0.0 --port 10000`.
6.  *Note:* Copy the generated `.onrender.com` URL.

### B. Frontend (InfinityFree)
1.  Login to your InfinityFree control panel.
2.  Upload `index.php` and `styles.css` from the `frontend/` folder to `htdocs`.
3.  **Critical**: In `index.php`, update the `$api_url` variable with your live Render URL:
    `$api_url = "https://your-app.onrender.com/predict";`
4.  Update the `fetch()` URL in the JavaScript status check section as well.

## 📡 API Reference

### POST `/predict`
Analyze an email string.
**Payload:** `{"email": "string"}`
**Response:**
```json
{
  "score": 85,
  "label": "STRONG EMAIL",
  "confidence": 0.85,
  "breakdown": {
    "personalization": 90,
    "clarity": 85,
    "relevance": 70,
    "tone": 90,
    "length": 100
  },
  "insights": ["Word Count: 45 (Optimal)", "Personalized greeting detected"],
  "suggestions": ["Great job! Ready for outreach."]
}
```

### GET `/health`
Check system status.
**Response:** `{"status": "running", "uptime_seconds": 120.5, "model_loaded": true}`

---
*Created with ❤️ for professional outreach teams.*
