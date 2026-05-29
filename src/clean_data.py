"""
clean_data.py
=============
Superstore Sales Analysis - Data Cleaning Script
Author: Armin R.
 
What this script does:
- Loads the raw Superstore CSV
- Cleans column names
- Fixes data types (dates, numbers)
- Adds useful derived columns
- Flags unprofitable orders
- Saves a clean CSV ready for analysis
"""
 
import pandas as pd
import os
 
# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "data", "superstore.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "superstore_clean.csv")
 
 
def load_data(path: str) -> pd.DataFrame:
    """Load raw CSV with correct encoding."""
    df = pd.read_csv(path, encoding="latin-1")
    print(f"✅ Loaded data: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df
 
 
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names: lowercase, underscores, no spaces."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    print("✅ Column names standardized")
    return df
 
 
def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert dates to datetime and ensure numeric columns are correct."""
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"]  = pd.to_datetime(df["ship_date"])
 
    df["sales"]    = df["sales"].astype(float).round(2)
    df["profit"]   = df["profit"].astype(float).round(2)
    df["discount"] = df["discount"].astype(float).round(2)
    df["quantity"] = df["quantity"].astype(int)
 
    print("✅ Data types fixed")
    return df
 
 
def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add useful columns for analysis."""
 
    # Time-based columns
    df["order_year"]    = df["order_date"].dt.year
    df["order_month"]   = df["order_date"].dt.month
    df["order_month_name"] = df["order_date"].dt.strftime("%b")  # Jan, Feb ...
    df["order_quarter"] = df["order_date"].dt.quarter.map(
        {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}
    )
 
    # Shipping duration (days between order and ship)
    df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
 
    # Profit margin per order (profit / sales)
    df["profit_margin"] = (df["profit"] / df["sales"]).round(4)
 
    # Revenue per unit
    df["revenue_per_unit"] = (df["sales"] / df["quantity"]).round(2)
 
    # Flag unprofitable orders
    df["is_unprofitable"] = df["profit"] < 0
 
    print("✅ Derived columns added: order_year, order_month, order_quarter,")
    print("   shipping_days, profit_margin, revenue_per_unit, is_unprofitable")
    return df
 
 
def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop columns not needed for analysis."""
    cols_to_drop = ["row_id", "country"]   # single country, row_id is just index
    df = df.drop(columns=cols_to_drop, errors="ignore")
    print(f"✅ Dropped unnecessary columns: {cols_to_drop}")
    return df
 
 
def validate_data(df: pd.DataFrame) -> None:
    """Print a validation report."""
    print("\n── Validation Report ─────────────────────────────────────────")
    print(f"   Rows            : {df.shape[0]:,}")
    print(f"   Columns         : {df.shape[1]}")
    print(f"   Missing values  : {df.isnull().sum().sum()}")
    print(f"   Duplicates      : {df.duplicated().sum()}")
    print(f"   Date range      : {df['order_date'].min().date()} → {df['order_date'].max().date()}")
    print(f"   Total sales     : ${df['sales'].sum():,.2f}")
    print(f"   Total profit    : ${df['profit'].sum():,.2f}")
    print(f"   Unprofitable orders: {df['is_unprofitable'].sum():,} "
          f"({df['is_unprofitable'].mean()*100:.1f}% of orders)")
    print("──────────────────────────────────────────────────────────────\n")
 
 
def save_clean_data(df: pd.DataFrame, path: str) -> None:
    """Save the cleaned DataFrame to CSV."""
    df.to_csv(path, index=False)
    print(f"✅ Clean data saved → {path}")
 
 
def main():
    print("\n🚀 Starting data cleaning...\n")
 
    df = load_data(INPUT_PATH)
    df = clean_column_names(df)
    df = fix_data_types(df)
    df = add_derived_columns(df)
    df = drop_unnecessary_columns(df)
 
    validate_data(df)
    save_clean_data(df, OUTPUT_PATH)
 
    print("🎉 Done! Clean file ready for analysis.\n")
 
 
if __name__ == "__main__":
    main()
 
