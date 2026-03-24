# Sentiment Analyzer

A lightweight, interactive sentiment analysis web app built with [Streamlit](https://streamlit.io). No API keys or model downloads required — everything runs locally.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- **Single text analysis** — paste any text and get instant sentiment feedback
- **Batch analysis** — analyze multiple texts at once (one per line)
- **Two models** — VADER, TextBlob, or run both side by side
- **Visualizations** — gauge charts, score breakdowns, and distribution bar charts
- **CSV export** — download batch results as a CSV file
- **Analysis history** — sidebar tracks your last 20 analyses per session

---

## Models

| Model | Best for | Extra metrics |
|---|---|---|
| **VADER** | Short text, social media, reviews | Compound, Positive, Neutral, Negative scores |
| **TextBlob** | General prose | Polarity + **Subjectivity** (0 = objective → 1 = subjective) |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

1. Clone the repository:

```bash
git clone https://github.com/fontainebrian/SentimentApp.git
cd SentimentApp
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (Git Bash)
source .venv/Scripts/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## Project Structure

```
SentimentApp/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `vaderSentiment` | VADER sentiment analysis |
| `textblob` | TextBlob sentiment analysis |
| `plotly` | Interactive charts |
| `pandas` | Batch results / CSV export |

---
