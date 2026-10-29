# Machine Learning Intrusion Detection Demo

This beginner project trains a simple machine-learning classifier on a **synthetic educational dataset** and presents results in a Streamlit dashboard. It is designed to teach the workflow: prepare data, train a model, evaluate it, and inspect predictions.

## Important limitation
The included data is synthetic and the model is for demonstration only. It does not detect real attacks reliably and must not be used as a production security control. Do not upload sensitive network captures or personal data.

## Run on Windows
Open a terminal in this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python generate_dataset.py
python train_model.py
streamlit run app.py
```

If PowerShell activation is blocked, use:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe generate_dataset.py
.\.venv\Scripts\python.exe train_model.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The browser should open automatically. If not, use the local address shown in the terminal.

## CSV format for your own demo data
Upload a CSV containing these columns:
- `duration`
- `src_bytes`
- `dst_bytes`
- `failed_logins`
- `connection_count`
- `label` (optional; values such as `normal` or `suspicious` are used for evaluation)

Rows without a `label` can be scored by the trained demo model. This app is not a replacement for professional IDS products or analyst review.
