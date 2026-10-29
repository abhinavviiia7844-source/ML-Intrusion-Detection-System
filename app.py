from pathlib import Path
import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sample_network_traffic.csv"
MODEL_PATH = BASE_DIR / "ids_model.joblib"
FEATURES = ["duration", "src_bytes", "dst_bytes", "failed_logins", "connection_count"]

st.set_page_config(page_title="Sentinel IDS | Demo", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #0b1220 0%, #101d31 100%); color: #eef4ff;}
[data-testid="stMetric"] {background: #15253a; padding: 18px; border: 1px solid #263c56; border-radius: 14px;}
div[data-testid="stDataFrame"] {border: 1px solid #263c56; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Sentinel IDS")
st.caption("Machine Learning Intrusion Detection · Educational Demo")

st.warning(
    "Demo only: the included model uses synthetic data and is not suitable for real-world threat detection. "
    "Treat predictions as examples, not security decisions."
)

if not MODEL_PATH.exists():
    st.error("Model file is missing. In this folder, run `python generate_dataset.py` and then `python train_model.py`.")
    st.stop()

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]

left, right = st.columns([1.1, 1])
with left:
    st.subheader("Analyze traffic data")
    st.write("Use the generated sample dataset or upload a CSV with the required feature columns.")
    use_sample = st.button("Load sample traffic data", type="primary")
    uploaded = st.file_uploader("Or upload a CSV file", type=["csv"])

if use_sample or (uploaded is None and "data_loaded" not in st.session_state):
    if DATA_PATH.exists():
        st.session_state["traffic_data"] = pd.read_csv(DATA_PATH)
        st.session_state["data_loaded"] = True

if uploaded is not None:
    try:
        candidate = pd.read_csv(uploaded)
        missing = [col for col in FEATURES if col not in candidate.columns]
        if missing:
            st.error("Missing required columns: " + ", ".join(missing))
        else:
            st.session_state["traffic_data"] = candidate
            st.session_state["data_loaded"] = True
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")

data = st.session_state.get("traffic_data")
if data is not None:
    missing = [col for col in FEATURES if col not in data.columns]
    if missing:
        st.error("Missing required columns: " + ", ".join(missing))
        st.stop()

    X = data[FEATURES].apply(pd.to_numeric, errors="coerce")
    result = data.copy()
    result["predicted_label"] = model.predict(X)
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X)
        classes = list(model.classes_)
        if "suspicious" in classes:
            result["suspicious_score_%"] = (probabilities[:, classes.index("suspicious")] * 100).round(1)
        else:
            result["suspicious_score_%"] = 0.0

    suspicious_count = int((result["predicted_label"] == "suspicious").sum())
    normal_count = int((result["predicted_label"] == "normal").sum())
    m1, m2, m3 = st.columns(3)
    m1.metric("Rows analyzed", f"{len(result):,}")
    m2.metric("Predicted normal", f"{normal_count:,}")
    m3.metric("Predicted suspicious", f"{suspicious_count:,}")

    st.subheader("Prediction overview")
    chart_col, table_col = st.columns([1, 1.6])
    with chart_col:
        counts = result["predicted_label"].value_counts()
        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax)
        ax.set_xlabel("Predicted class")
        ax.set_ylabel("Number of rows")
        ax.set_title("Traffic classification")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    with table_col:
        st.write("Preview of analyzed rows")
        st.dataframe(result.head(100), use_container_width=True, hide_index=True)

    csv = result.to_csv(index=False).encode("utf-8")
    st.download_button("Download predictions as CSV", csv, "ids_predictions.csv", "text/csv")

    if "label" in result.columns:
        st.subheader("Optional comparison with labels")
        st.caption("If your CSV has a `label` column, compare it with the model's predictions. This is only meaningful when labels are trustworthy.")
        st.dataframe(
            result[["label", "predicted_label"]].value_counts().rename("rows").reset_index(),
            use_container_width=True,
            hide_index=True,
        )
else:
    st.info("Click **Load sample traffic data** to begin.")

with right:
    st.subheader("Features used")
    st.markdown("""
    - **duration** — connection duration (demo feature)
    - **src_bytes** — bytes sent from source
    - **dst_bytes** — bytes sent to destination
    - **failed_logins** — failed login attempts (demo feature)
    - **connection_count** — connection count in the sample window
    """)
    st.subheader("How it works")
    st.markdown("""
    1. Load traffic feature rows.
    2. The trained Random Forest model predicts a class.
    3. Review the table and export results.
    4. Validate any real alert using trusted security tools and human analysis.
    """)
    st.info("For learning only. The dataset is generated and does not represent real captured network traffic.")
