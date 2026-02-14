"""
Download dataset from Kaggle.

For CI/CD: Uses GitHub Secrets (KAGGLE_USERNAME, KAGGLE_KEY)
For local: Requires ~/.kaggle/kaggle.json
"""

import os
import subprocess
from pathlib import Path


def download_dataset():
    raw_data_path = Path(__file__).parent / "raw"
    raw_data_path.mkdir(parents=True, exist_ok=True)
    
    print("Downloading dataset from Kaggle...")
    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", "hassanjameelahmed/price-of-healthy-diet-clean",
        "-p", str(raw_data_path),
        "--unzip"
    ])
    print(f"Done! Data saved to {raw_data_path}")


if __name__ == "__main__":
    download_dataset()