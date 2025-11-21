import json
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample.csv"
META_FILE = PROJECT_ROOT / "model" / "metadata.json"


def compute_file_hash(path: Path, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    print(f"Validating model metadata at {META_FILE}")

    if not META_FILE.exists():
        print(f"[ERROR] metadata.json not found at {META_FILE}")
        return

    with META_FILE.open("r", encoding="utf-8") as f:
        meta = json.load(f)

    required = ["model_version", "dataset_hash", "training_date", "hash_algorithm"]

    for key in required:
        if key not in meta:
            print(f"[ERROR] Missing key in metadata: {key}")
        else:
            print(f"[OK] {key}: {meta[key]}")

    if not DATA_PATH.exists():
        print(f"[ERROR] Dataset not found at {DATA_PATH}")
        return

    print("\nChecking dataset integrity...")
    current_hash = compute_file_hash(DATA_PATH, meta.get("hash_algorithm", "sha256"))

    if current_hash == meta["dataset_hash"]:
        print("[OK] Dataset hash matches metadata")
    else:
        print("[ERROR] Dataset hash mismatch")
        print(f"Expected: {meta['dataset_hash']}")
        print(f"Actual  : {current_hash}")


if __name__ == "__main__":
    main()
