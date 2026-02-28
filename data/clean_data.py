"""
Cleans the "price_of_healthy_diet" dataset by joining with country code lookup table.
"""

import os
from pathlib import Path
import pandas as pd


def clean_dataset():
    """
    Load and clean the price_of_healthy_diet data by joining with country code lookups.
    
    Returns:
        pd.DataFrame: Cleaned dataset with country information joined from lookup table.
    """
    # Define file paths
    raw_data_path = Path(__file__).parent / "raw" / "price_of_healthy_diet_clean.csv"
    lookup_path = Path(__file__).parent / "lookups" / "country_codes.csv"
    
    # Load raw data
    df_price = pd.read_csv(raw_data_path)
    
    # Load country codes lookup
    df_lookup = pd.read_csv(lookup_path)
    

    # Data Cleaning -->
    
    # 1) Join on country_code (Numeric column in lookup)
    print("Joining datasets on country code...")
    df_clean = df_price.merge(
        df_lookup,
        left_on="country_code",
        right_on="Numeric",
        how="left"
    )
    
    # Define output path
    output_dir = Path(__file__).parent / "processed"
    output_path = output_dir / "cleaned_price_of_healthy_diet.csv"

    # Ensure the directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the dataframe
    df_clean.to_csv(output_path, index=False)
    print(f"File saved to: {output_path}")

    return df_clean

if __name__ == "__main__":
    clean_dataset()