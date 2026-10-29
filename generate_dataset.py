from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def main():
    rng = np.random.default_rng(42)
    rows = 1200
    labels = rng.choice(["normal", "suspicious"], size=rows, p=[0.72, 0.28])
    records = []
    for label in labels:
        if label == "normal":
            duration = rng.gamma(2.2, 18)
            src_bytes = rng.lognormal(7.1, 0.9)
            dst_bytes = rng.lognormal(7.4, 0.9)
            failed_logins = rng.poisson(0.15)
            connection_count = rng.poisson(5) + 1
        else:
            duration = rng.gamma(1.2, 5)
            src_bytes = rng.lognormal(5.8, 1.1)
            dst_bytes = rng.lognormal(5.2, 1.2)
            failed_logins = rng.poisson(3.2)
            connection_count = rng.poisson(17) + 4
        records.append({
            "duration": round(float(duration), 3),
            "src_bytes": int(src_bytes),
            "dst_bytes": int(dst_bytes),
            "failed_logins": int(failed_logins),
            "connection_count": int(connection_count),
            "label": label,
        })
    path = DATA_DIR / "sample_network_traffic.csv"
    pd.DataFrame(records).to_csv(path, index=False)
    print(f"Created {len(records)} synthetic demo rows at: {path}")


if __name__ == "__main__":
    main()
