import pandas as pd
from pathlib import Path

def get_data():
    # project_root/data/raw
    data_path = Path(__file__).parent.parent / "data" / "raw"
    csv_path = data_path / "price_of_healthy_diet_clean.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV not found at {csv_path}. Make sure dataset exists in data/raw/"
        )

    df = pd.read_csv(csv_path)

    print("DATA LOADED")
    print("Rows:", len(df))
    print("Columns:", df.columns)

    return df
