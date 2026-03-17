"""
Cleans the "price_of_healthy_diet" dataset by joining with country code lookup table
and fixing regions/continents using a countries-by-continent lookup.
"""

from pathlib import Path
import unicodedata

import pandas as pd

def _normalize_country_names(country_series: pd.Series) -> pd.Series:
    """standardize country names to match countries_by_continents lookup"""

    name_map = {
        "Burkina Faso": "Burkina",
        "Bolivia (Plurinational State of)": "Bolivia",
        "Brunei Darussalam": "Brunei",
        "Cabo Verde": "Cape Verde",
        "China, mainland": "China",
        "China, Hong Kong SAR": "Hong Kong",
        "China, Taiwan Province of": "Taiwan",
        "Côte d'Ivoire": "Ivory Coast",
        "Democratic Republic of the Congo": "Democratic Republic of Congo",
        "Eswatini": "Swaziland",
        "Iran (Islamic Republic of)": "Iran",
        "Lao People's Democratic Republic": "Laos",
        "Myanmar": "Burma (Myanmar)",
        "North Macedonia": "Macedonia",
        "Republic of Korea": "South Korea",
        "Republic of Moldova": "Moldova",
        "Russian Federation": "Russia",
        "Syrian Arab Republic": "Syria",
        "Türkiye": "Turkey",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "United Republic of Tanzania": "Tanzania",
        "United States of America": "United States",
        "Viet Nam": "Vietnam",
        "Netherlands (Kingdom of the)": "Netherlands",
    }

    def _canon(s: str) -> str:
        # normalize unicode and punctuation for consistent matching
        s = unicodedata.normalize("NFKC", s)
        s = s.replace("\u2019", "'").replace("\u2018", "'")
        s = s.replace("\u00a0", " ")
        return s.strip()

    return country_series.astype(str).map(_canon).replace(name_map)


def clean_dataset() -> pd.DataFrame:
    """
    Load and clean the price_of_healthy_diet data by joining with country code lookups,
    then fix region using countries_by_continent lookup.

    Returns:
        pd.DataFrame: Cleaned dataset with country information and corrected region.
    """
    project_root = Path(__file__).resolve().parents[1]

    raw_data_path = project_root / "data" / "raw" / "price_of_healthy_diet_clean.csv"
    country_codes_path = project_root / "data" / "lookups" / "country_codes.csv"
    continent_lookup_path = project_root / "data" / "lookups" / "countries_by_continents.csv"

    df_price = pd.read_csv(raw_data_path)
    df_codes = pd.read_csv(country_codes_path)
    df_continent = pd.read_csv(continent_lookup_path)

    # 1) join on country_code (Numeric column in lookup)
    print("Joining datasets on country code...")
    codes_keep = ["Numeric", "Alpha-2 code", "Alpha-3 code"]
    df_clean = df_price.merge(
        df_codes[codes_keep],
        left_on="country_code",
        right_on="Numeric",
        how="left",
    )

    # 2) fix region using countries_by_continent.csv
    # keep original region for debugging
    df_clean["region_original"] = df_clean["region"]

    # normalize country names to match the lookup
    df_clean["country_for_lookup"] = _normalize_country_names(df_clean["country"])

    # standardize country names in the final dataset as well (not just for lookup!)
    df_clean["country"] = df_clean["country_for_lookup"]

    # ensure lookup columns are named consistently -> expected: Continent, Country
    if not {"Continent", "Country"}.issubset(df_continent.columns):
        raise ValueError(
            "countries_by_continent.csv must contain columns: 'Country' and 'Continent'."
        )

    # merge continent onto df_clean
    df_clean = df_clean.merge(
        df_continent[["Country", "Continent"]],
        left_on="country_for_lookup",
        right_on="Country",
        how="left",
    )

    # manual continent overrides for territories missing from the lookup
    manual_continent_overrides = {
        "Aruba": "North America",
        "Bermuda": "North America",
        "British Virgin Islands": "North America",
        "Cayman Islands": "North America",
        "Curaçao": "North America",
        "Sint Maarten (Dutch part)": "North America",
        "Turks and Caicos Islands": "North America",
        "Palestine": "Asia",
    }
    df_clean["Continent"] = df_clean["Continent"].fillna(
        df_clean["country"].map(manual_continent_overrides)
    )

    # replace region with corrected continent where available
    df_clean["region"] = df_clean["Continent"].fillna(df_clean["region"])

    # report unmatched countries (still missing Continent after overrides)
    unmatched = (
        df_clean.loc[df_clean["Continent"].isna(), "country_for_lookup"]
        .dropna()
        .unique()
        .tolist()
    )
    if len(unmatched) > 0:
        unmatched = sorted(unmatched)
        print("Warning: some countries did not match countries_by_continent lookup:")
        print(unmatched)

    # drop helper columns + merge helper columns
    df_clean = df_clean.drop(
        columns=[
            "Country",
            "Continent",
            "country_for_lookup",
            "Numeric",
            "Alpha-2 code",
            "region_original",
        ],
        errors="ignore",
    )

    # define output path
    output_dir = project_root / "data" / "processed"
    output_path = output_dir / "cleaned_price_of_healthy_diet.csv"

    # ensure the directory exists
    output_dir.mkdir(parents=True, exist_ok=True)


    # save the dataframe
    df_clean.to_csv(output_path, index=False)
    print(f"CSV saved to: {output_path}")

    parquet_path = output_dir / "cleaned_price_of_healthy_diet.parquet"
    df_clean.to_parquet(parquet_path, index=False)
    print(f"Parquet saved to: {parquet_path}")

    return df_clean


if __name__ == "__main__":
    clean_dataset()