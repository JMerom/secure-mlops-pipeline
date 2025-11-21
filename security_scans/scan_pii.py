import sys
from pathlib import Path

import pandas as pd
from presidio_analyzer import AnalyzerEngine


def scan_file(path: Path) -> None:
    df = pd.read_csv(path)
    analyzer = AnalyzerEngine()

    print(f"Scanning file for PII: {path}")
    print(f"Columns: {list(df.columns)}\n")

    hits = 0

    for col in df.columns:
        for i, val in enumerate(df[col].astype(str)):
            results = analyzer.analyze(text=val, language="en")
            if results:
                hits += 1
                entities = ", ".join(r.entity_type for r in results)
                print(
                    f"[PII DETECTED] row={i} col={col} value={val[:30]}... entities={entities}"
                )

    if hits == 0:
        print("No PII detected according to the configured models.")
    else:
        print(f"\nTotal potential PII hits: {hits}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python scan_pii.py <csv_path>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    scan_file(path)


if __name__ == "__main__":
    main()
