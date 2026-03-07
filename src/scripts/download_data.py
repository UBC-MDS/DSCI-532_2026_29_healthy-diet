"""
Download datasets from Kaggle.

For CI/CD: Uses GitHub Secrets (KAGGLE_USERNAME, KAGGLE_KEY)
For local: Requires ~/.kaggle/kaggle.json
"""

import subprocess
from pathlib import Path


def download_dataset():
    project_root = Path(__file__).resolve().parents[1]

    raw_data_path = project_root / "data" / "raw"
    lookup_data_path = project_root / "data" / "lookups"

    raw_data_path.mkdir(parents=True, exist_ok=True)
    lookup_data_path.mkdir(parents=True, exist_ok=True)

    # download price of healthy diet dataset
    print("Downloading price-of-healthy-diet-clean from Kaggle...")
    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", "hassanjameelahmed/price-of-healthy-diet-clean",
        "-p", str(raw_data_path),
        "--unzip"
    ], check=True)

if __name__ == "__main__":
    download_dataset()