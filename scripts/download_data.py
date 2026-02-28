"""
Download datasets from Kaggle.

For CI/CD: Uses GitHub Secrets (KAGGLE_USERNAME, KAGGLE_KEY)
For local: Requires ~/.kaggle/kaggle.json
"""

import subprocess
from pathlib import Path


def download_dataset():
    raw_data_path = Path(__file__).parent / "raw"
    raw_data_path.mkdir(parents=True, exist_ok=True)

    # download price of healthy diet dataset
    print("Downloading price-of-healthy-diet-clean from Kaggle...")
    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", "hassanjameelahmed/price-of-healthy-diet-clean",
        "-p", str(raw_data_path),
        "--unzip"
    ], check=True)

    # download countries-by-continent lookup dataset
    print("Downloading countries-by-continent from Kaggle...")
    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", "hserdaraltan/countries-by-continent",
        "-p", str(raw_data_path),
        "--unzip"
    ], check=True)

    print(f"Done! Data saved to {raw_data_path}")


if __name__ == "__main__":
    download_dataset()