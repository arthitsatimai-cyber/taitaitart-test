"""
Data Loading, Data Cleaning, and Data Filtering Utilities
"""

import os
from typing import List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import streamlit as st

SAMPLE_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "sample_sales.csv"
)


def load_sample_data() -> pd.DataFrame:
    """Load sample sales data from local CSV file."""
    if not os.path.exists(SAMPLE_DATA_PATH):
        st.error(f"ไม่พบไฟล์ข้อมูลตัวอย่างที่: {SAMPLE_DATA_PATH}")
        return pd.DataFrame()

    try:
        df = pd.read_csv(SAMPLE_DATA_PATH, encoding="utf-8-sig")
        return df
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูลตัวอย่าง: {e}")
        return pd.DataFrame()


def load_uploaded_data(uploaded_file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Load data from an uploaded CSV or Excel file.
    Returns (DataFrame, ErrorMessage).
    """
    if uploaded_file is None:
        return None, "กรุณาอัปโหลดไฟล์"

    file_name = uploaded_file.name.lower()
    try:
        if file_name.endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding="tis-620")
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "รูปแบบไฟล์ไม่รองรับ! กรุณาอัปโหลดไฟล์ .csv หรือ .xlsx"

        required_cols = [
            "order_id",
            "order_date",
            "branch",
            "category",
            "product_name",
            "quantity",
            "unit_price",
            "discount_rate",
            "payment_method",
        ]

        # Check missing required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return None, f"คอลัมน์ไม่ครบถ้วน! ขาดคอลัมน์: {', '.join(missing_cols)}"

        return df, None

    except Exception as e:
        return None, f"เกิดข้อผิดพลาดในการอ่านไฟล์: {str(e)}"


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw sales data:
    1. Remove duplicates
    2. Convert order_date to datetime
    3. Fill missing values
    4. Convert data types
    5. Calculate Net Sales: quantity * unit_price * (1 - discount_rate)
    """
    if df is None or df.empty:
        return pd.DataFrame()

    df_clean = df.copy()

    # 1. Remove duplicates
    df_clean = df_clean.drop_duplicates()

    # 2. Convert order_date
    df_clean["order_date"] = pd.to_datetime(df_clean["order_date"], errors="coerce")

    # Drop rows with invalid date
    df_clean = df_clean.dropna(subset=["order_date"])

    # 3. Fill missing values
    df_clean["quantity"] = pd.to_numeric(df_clean["quantity"], errors="coerce").fillna(1)
    df_clean["unit_price"] = pd.to_numeric(df_clean["unit_price"], errors="coerce").fillna(0.0)
    df_clean["discount_rate"] = pd.to_numeric(df_clean["discount_rate"], errors="coerce").fillna(0.0)

    df_clean["branch"] = df_clean["branch"].fillna("ไม่ระบุสาขา")
    df_clean["category"] = df_clean["category"].fillna("ทาร์ตไข่")
    df_clean["product_name"] = df_clean["product_name"].fillna("สินค้าไม่ระบุ")
    df_clean["payment_method"] = df_clean["payment_method"].fillna("Cash")

    # 4. Correct data types
    df_clean["quantity"] = df_clean["quantity"].astype(int)
    df_clean["unit_price"] = df_clean["unit_price"].astype(float)
    df_clean["discount_rate"] = df_clean["discount_rate"].astype(float)

    # 5. Calculate Net Sales
    df_clean["net_sales"] = (
        df_clean["quantity"] * df_clean["unit_price"] * (1.0 - df_clean["discount_rate"])
    )

    return df_clean


def filter_data(
    df: pd.DataFrame,
    date_range: Optional[Tuple[pd.Timestamp, pd.Timestamp]] = None,
    selected_branches: Optional[List[str]] = None,
    selected_products: Optional[List[str]] = None,
    selected_payments: Optional[List[str]] = None,
    sales_range: Optional[Tuple[float, float]] = None,
) -> pd.DataFrame:
    """Filter DataFrame according to sidebar criteria."""
    if df is None or df.empty:
        return pd.DataFrame()

    filtered_df = df.copy()

    # Filter by date range
    if date_range and len(date_range) == 2 and date_range[0] and date_range[1]:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered_df = filtered_df[
            (filtered_df["order_date"] >= start_date) & (filtered_df["order_date"] <= end_date)
        ]

    # Filter by branch
    if selected_branches:
        filtered_df = filtered_df[filtered_df["branch"].isin(selected_branches)]

    # Filter by product name
    if selected_products:
        filtered_df = filtered_df[filtered_df["product_name"].isin(selected_products)]

    # Filter by payment method
    if selected_payments:
        filtered_df = filtered_df[filtered_df["payment_method"].isin(selected_payments)]

    # Filter by sales range
    if sales_range and len(sales_range) == 2:
        min_sale, max_sale = sales_range
        filtered_df = filtered_df[
            (filtered_df["net_sales"] >= min_sale) & (filtered_df["net_sales"] <= max_sale)
        ]

    return filtered_df
