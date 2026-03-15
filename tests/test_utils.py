import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from app import format_cost, _click_js

# Test 1: _click_js returns valid javascript 

def test_click_js_returns_string():
    """_click_js should return a non-empty JavaScript string."""
    result = _click_js("my_div", "my_input", "pt.x")
    assert isinstance(result, str)
    assert len(result) > 0

def test_click_js_contains_div_id():
    """_click_js output should reference the provided div ID."""
    result = _click_js("map_plot", "map_click", "pt.hovertext")
    assert "map_plot" in result

def test_click_js_contains_shiny_input():
    """_click_js output should reference the provided Shiny input name."""
    result = _click_js("map_plot", "map_click", "pt.hovertext")
    assert "map_click" in result

# Test 2: Parquet data loads in a correct way

def test_data_loads_with_expected_columns():
    """Processed parquet file should contain key columns."""
    df = pd.read_parquet("src/data/processed/cleaned_price_of_healthy_diet.parquet")
    expected_cols = ["country", "year", "cost_healthy_diet_ppp_usd", "region"]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"

def test_data_has_no_null_countries():
    """Country column should have no null values."""
    df = pd.read_parquet("src/data/processed/cleaned_price_of_healthy_diet.parquet")
    assert df["country"].isnull().sum() == 0

def test_data_year_range():
    """Year range should span from 2017 to 2024."""
    df = pd.read_parquet("src/data/processed/cleaned_price_of_healthy_diet.parquet")
    assert df["year"].min() == 2017
    assert df["year"].max() == 2024

# Test 3: Return correct values of cost after refactor

def test_format_cost_mean():
    """Should return formatted mean cost."""
    s = pd.Series([1.0, 2.0, 3.0])
    assert format_cost(s, "mean") == "$2.00"

def test_format_cost_min():
    """Should return formatted min cost."""
    s = pd.Series([1.0, 2.0, 3.0])
    assert format_cost(s, "min") == "$1.00"

def test_format_cost_max():
    """Should return formatted max cost."""
    s = pd.Series([1.0, 2.0, 3.0])
    assert format_cost(s, "max") == "$3.00"

def test_format_cost_empty():
    """Should return dash for empty series."""
    s = pd.Series([], dtype=float)
    assert format_cost(s) == "—"