import json
import hashlib
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample.csv"
MODEL_DIR = PROJECT_ROOT / "model"
MODEL_FILE = MODEL_DIR / "model.pkl"
META_FILE = MODEL_DIR / "metadata.json"


def compute_file_hash(path: Path, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    print(f"Loading dataset from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    target_col = "target_segment"
    feature_cols = [c for c in df.columns if c != target_col]

    X = df[feature_cols]
    y = df[target_col]

    num_cols = [c for c in X.columns if X[c].dtype != "object"]
    cat_cols = [c for c in X.columns if X[c].dtype == "object"]

    numeric_transformer = "passthrough"
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ]
    )

    clf = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", LogisticRegression(max_iter=1000)),
        ]
    )

    print("Training model...")
    clf.fit(X, y)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")

    data_hash = compute_file_hash(DATA_PATH)
    metadata = {
        "model_version": "1.0.0",
        "model_type": "LogisticRegression",
        "training_date": datetime.utcnow().isoformat() + "Z",
        "dataset_path": str(DATA_PATH.relative_to(PROJECT_ROOT)),
        "dataset_hash": data_hash,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "target_column": target_col,
        "feature_columns": feature_cols,
        "hash_algorithm": "sha256",
    }

    with META_FILE.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved to {META_FILE}")
    print("Training complete.")


if __name__ == "__main__":
    main()
