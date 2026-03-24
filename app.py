import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🔍",
    layout="wide",
)

# --- Styling ---
st.markdown("""
<style>
.sentiment-positive { color: #2ecc71; font-size: 2rem; font-weight: 700; }
.sentiment-negative { color: #e74c3c; font-size: 2rem; font-weight: 700; }
.sentiment-neutral  { color: #95a5a6; font-size: 2rem; font-weight: 700; }
.score-label { font-size: 0.85rem; color: #888; }
</style>
""", unsafe_allow_html=True)

# --- Helpers ---
analyzer = SentimentIntensityAnalyzer()

def analyze_vader(text: str) -> dict:
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label, css = "Positive", "sentiment-positive"
    elif compound <= -0.05:
        label, css = "Negative", "sentiment-negative"
    else:
        label, css = "Neutral", "sentiment-neutral"
    return {**scores, "label": label, "css": css}

def analyze_textblob(text: str) -> dict:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity          # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1
    if polarity > 0.05:
        label, css = "Positive", "sentiment-positive"
    elif polarity < -0.05:
        label, css = "Negative", "sentiment-negative"
    else:
        label, css = "Neutral", "sentiment-neutral"
    return {"polarity": polarity, "subjectivity": subjectivity, "label": label, "css": css}

def gauge_chart(value: float, title: str) -> go.Figure:
    """Compound / polarity gauge from -1 to 1."""
    color = "#2ecc71" if value >= 0.05 else "#e74c3c" if value <= -0.05 else "#95a5a6"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 16}},
        number={"font": {"size": 28}},
        gauge={
            "axis": {"range": [-1, 1], "tickwidth": 1},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "white",
            "borderwidth": 2,
            "steps": [
                {"range": [-1, -0.05], "color": "#fdecea"},
                {"range": [-0.05, 0.05], "color": "#f5f5f5"},
                {"range": [0.05, 1],  "color": "#e8f8f0"},
            ],
            "threshold": {
                "line": {"color": color, "width": 4},
                "thickness": 0.8,
                "value": value,
            },
        },
    ))
    fig.update_layout(height=250, margin=dict(t=40, b=10, l=20, r=20))
    return fig

def score_bar_chart(pos: float, neu: float, neg: float) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=[pos, neu, neg],
        y=["Positive", "Neutral", "Negative"],
        orientation="h",
        marker_color=["#2ecc71", "#95a5a6", "#e74c3c"],
        text=[f"{v:.3f}" for v in [pos, neu, neg]],
        textposition="outside",
    ))
    fig.update_layout(
        height=200,
        margin=dict(t=10, b=10, l=10, r=40),
        xaxis=dict(range=[0, 1], showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("Sentiment Analyzer")
st.caption("Powered by VADER & TextBlob — runs entirely in your browser session, no API required.")

mode = st.radio("Mode", ["Single Text", "Batch (one per line)"], horizontal=True)

# --- Session history ---
if "history" not in st.session_state:
    st.session_state.history = []

# ── Single Text Mode ──────────────────────────────────────────────────────────
if mode == "Single Text":
    text_input = st.text_area(
        "Enter text to analyze",
        height=150,
        placeholder="Type or paste any text here…",
    )

    model_choice = st.selectbox("Analysis model", ["VADER (recommended)", "TextBlob", "Both"])

    col_btn, _ = st.columns([1, 5])
    with col_btn:
        analyze_clicked = st.button("Analyze", type="primary", use_container_width=True)

    if analyze_clicked and text_input.strip():
        st.divider()

        use_vader = model_choice in ("VADER (recommended)", "Both")
        use_blob  = model_choice in ("TextBlob", "Both")

        if use_vader:
            v = analyze_vader(text_input)
            st.session_state.history.append({"text": text_input[:80], "model": "VADER",
                                              "label": v["label"], "score": v["compound"]})

            st.subheader("VADER Results")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f'<p class="{v["css"]}">{v["label"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<span class="score-label">Compound score: **{v["compound"]:.4f}**</span>',
                            unsafe_allow_html=True)
                st.plotly_chart(gauge_chart(v["compound"], "Compound Score"),
                                use_container_width=True, key="vader_gauge")
            with col2:
                st.markdown("##### Score Breakdown")
                st.plotly_chart(score_bar_chart(v["pos"], v["neu"], v["neg"]),
                                use_container_width=True, key="vader_bars")
                metrics_cols = st.columns(4)
                for col, key, label in zip(metrics_cols,
                                           ["compound", "pos", "neu", "neg"],
                                           ["Compound", "Positive", "Neutral", "Negative"]):
                    col.metric(label, f"{v[key]:.4f}")

        if use_blob:
            b = analyze_textblob(text_input)
            if use_vader:
                st.divider()
            st.session_state.history.append({"text": text_input[:80], "model": "TextBlob",
                                              "label": b["label"], "score": b["polarity"]})

            st.subheader("TextBlob Results")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f'<p class="{b["css"]}">{b["label"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<span class="score-label">Polarity: **{b["polarity"]:.4f}**</span>',
                            unsafe_allow_html=True)
                st.plotly_chart(gauge_chart(b["polarity"], "Polarity"),
                                use_container_width=True, key="blob_gauge")
            with col2:
                st.markdown("##### Sentiment Metrics")
                c1, c2 = st.columns(2)
                c1.metric("Polarity", f"{b['polarity']:.4f}",
                          help="−1 (very negative) → +1 (very positive)")
                c2.metric("Subjectivity", f"{b['subjectivity']:.4f}",
                          help="0 (objective) → 1 (subjective)")

    elif analyze_clicked:
        st.warning("Please enter some text before analyzing.")

# ── Batch Mode ────────────────────────────────────────────────────────────────
else:
    batch_input = st.text_area(
        "Enter one sentence / document per line",
        height=200,
        placeholder="The product is great!\nTerrible experience, would not recommend.\nIt was okay.",
    )

    col_btn, _ = st.columns([1, 5])
    with col_btn:
        batch_clicked = st.button("Analyze All", type="primary", use_container_width=True)

    if batch_clicked and batch_input.strip():
        lines = [l.strip() for l in batch_input.splitlines() if l.strip()]
        results = []
        for line in lines:
            v = analyze_vader(line)
            b = analyze_textblob(line)
            results.append({
                "Text": line[:80] + ("…" if len(line) > 80 else ""),
                "VADER Label": v["label"],
                "VADER Compound": round(v["compound"], 4),
                "TextBlob Label": b["label"],
                "TextBlob Polarity": round(b["polarity"], 4),
                "Subjectivity": round(b["subjectivity"], 4),
            })

        df = pd.DataFrame(results)
        st.divider()
        st.subheader(f"Results — {len(df)} texts analyzed")

        # Summary counts
        vader_counts = df["VADER Label"].value_counts()
        cols = st.columns(3)
        for i, sentiment in enumerate(["Positive", "Negative", "Neutral"]):
            cols[i].metric(sentiment, vader_counts.get(sentiment, 0))

        # Distribution chart
        fig_dist = go.Figure(go.Bar(
            x=["Positive", "Negative", "Neutral"],
            y=[vader_counts.get(s, 0) for s in ["Positive", "Negative", "Neutral"]],
            marker_color=["#2ecc71", "#e74c3c", "#95a5a6"],
        ))
        fig_dist.update_layout(
            title="Sentiment Distribution (VADER)",
            height=300,
            margin=dict(t=40, b=10, l=10, r=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_dist, use_container_width=True)

        # Full table
        st.markdown("##### Detailed Results")

        def highlight_label(val):
            colors = {"Positive": "#d4edda", "Negative": "#f8d7da", "Neutral": "#e2e3e5"}
            return f"background-color: {colors.get(val, '')}"

        st.dataframe(
            df.style.applymap(highlight_label, subset=["VADER Label", "TextBlob Label"]),
            use_container_width=True,
            hide_index=True,
        )

        csv = df.to_csv(index=False).encode()
        st.download_button("Download CSV", csv, "sentiment_results.csv", "text/csv")

    elif batch_clicked:
        st.warning("Please enter at least one line of text.")


# ── History Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Analysis History")
    if st.session_state.history:
        if st.button("Clear history"):
            st.session_state.history = []
            st.rerun()
        for i, item in enumerate(reversed(st.session_state.history[-20:])):
            label_colors = {"Positive": "🟢", "Negative": "🔴", "Neutral": "⚪"}
            icon = label_colors.get(item["label"], "●")
            with st.expander(f"{icon} {item['label']} — {item['text'][:40]}…", expanded=False):
                st.write(f"**Model:** {item['model']}")
                st.write(f"**Score:** {item['score']:.4f}")
                st.write(f"**Text:** {item['text']}")
    else:
        st.caption("Analyzed texts will appear here.")
