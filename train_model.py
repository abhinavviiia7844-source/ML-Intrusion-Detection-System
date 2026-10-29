from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sample_network_traffic.csv"
MODEL_PATH = BASE_DIR / "ids_model.joblib"
FEATURES = ["duration", "src_bytes", "dst_bytes", "failed_logins", "connection_count"]


def main():
    if not DATA_PATH.exists():
        raise SystemExit("Dataset not found. Run: python generate_dataset.py")
    data = pd.read_csv(DATA_PATH)
    X = data[FEATURES]
    y = data["label"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(
            n_estimators=120, random_state=42, class_weight="balanced"
        )),
    ])
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(f"Test accuracy (synthetic data only): {accuracy_score(y_test, predictions):.3f}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))
    print("Confusion matrix (label order shown by sklearn):")
    print(confusion_matrix(y_test, predictions))
    joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH)
    print(f"\nSaved model to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
