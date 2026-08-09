"""
Analytics and Statistical Calculation Utilities
"""

from typing import Dict, Any, Tuple
import pandas as pd


def calculate_kpis(df: pd.DataFrame, target_sales: float = 150000.0) -> Dict[str, Any]:
    """
    Calculate core business KPIs from cleaned sales dataframe:
    - Total Net Sales (ยอดขายสุทธิรวม)
    - Total Orders (จำนวนรายการขาย)
    - Total Items Sold (จำนวนสินค้าที่ขายได้)
    - Average Order Value (มูลค่าเฉลี่ยต่อรายการ)
    - Top Product by Sales (สินค้ามียอดขายสูงสุด)
    - Sales vs Target Percentage (เปอร์เซ็นต์เทียบกับเป้าหมาย)
    """
    if df is None or df.empty:
        return {
            "total_sales": 0.0,
            "total_orders": 0,
            "total_units": 0,
            "avg_order_value": 0.0,
            "top_product": "ไม่มีข้อมูล",
            "top_product_sales": 0.0,
            "target_sales": target_sales,
            "target_pct": 0.0,
        }

    total_sales = float(df["net_sales"].sum())
    total_orders = int(df["order_id"].nunique())
    total_units = int(df["quantity"].sum())
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0
    target_pct = (total_sales / target_sales * 100) if target_sales > 0 else 0.0

    # Top selling product by revenue
    product_sales = df.groupby("product_name")["net_sales"].sum().reset_index()
    if not product_sales.empty:
        top_row = product_sales.sort_values(by="net_sales", ascending=False).iloc[0]
        top_product = str(top_row["product_name"])
        top_product_sales = float(top_row["net_sales"])
    else:
        top_product = "ไม่มีข้อมูล"
        top_product_sales = 0.0

    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "total_units": total_units,
        "avg_order_value": avg_order_value,
        "top_product": top_product,
        "top_product_sales": top_product_sales,
        "target_sales": target_sales,
        "target_pct": target_pct,
    }


def get_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Group sales by order_date."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["order_date", "net_sales"])
    daily = df.groupby("order_date")["net_sales"].sum().reset_index()
    return daily.sort_values(by="order_date")


def get_sales_by_branch(df: pd.DataFrame) -> pd.DataFrame:
    """Group sales by branch."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["branch", "net_sales"])
    branch_sales = df.groupby("branch")["net_sales"].sum().reset_index()
    return branch_sales.sort_values(by="net_sales", ascending=False)


def get_sales_by_product(df: pd.DataFrame) -> pd.DataFrame:
    """Group sales by product_name."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["product_name", "net_sales", "quantity"])
    prod_sales = df.groupby("product_name").agg({"net_sales": "sum", "quantity": "sum"}).reset_index()
    return prod_sales.sort_values(by="net_sales", ascending=False)


def get_top_products(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Get Top N best-selling products by net sales."""
    df_prod = get_sales_by_product(df)
    return df_prod.head(top_n)


def get_sales_by_payment(df: pd.DataFrame) -> pd.DataFrame:
    """Group sales by payment_method."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["payment_method", "net_sales"])
    pay_sales = df.groupby("payment_method")["net_sales"].sum().reset_index()
    return pay_sales.sort_values(by="net_sales", ascending=False)


def generate_business_insights(df: pd.DataFrame, target_sales: float = 150000.0) -> list:
    """Generate business insights and actionable recommendations based on filtered sales data."""
    if df is None or df.empty:
        return ["⚠️ ไม่มีข้อมูลเพียงพอสำหรับการสรุปผลวิเคราะห์"]

    insights = []
    total_sales = float(df["net_sales"].sum())
    
    # 1. Target Comparison Insight
    diff = total_sales - target_sales
    if diff >= 0:
        insights.append(f"🎯 **เป้าหมายยอดขาย:** ทำยอดขายได้ **฿{total_sales:,.2f}** ทะลุเป้าหมาย **฿{target_sales:,.2f}** คิดเป็น **{total_sales/target_sales*100:.1f}%** ของเป้า (เกินเป้าอยู่ ฿{diff:,.2f})")
    else:
        insights.append(f"🎯 **เป้าหมายยอดขาย:** ยอดขายปัจจุบัน **฿{total_sales:,.2f}** ยังขาดอีก **฿{abs(diff):,.2f}** (คิดเป็น **{total_sales/target_sales*100:.1f}%** ของเป้าหมาย ฿{target_sales:,.2f})")

    # 2. Branch Performance Insight
    branch_df = get_sales_by_branch(df)
    if not branch_df.empty:
        best_branch = branch_df.iloc[0]['branch']
        best_branch_sales = branch_df.iloc[0]['net_sales']
        best_branch_pct = (best_branch_sales / total_sales) * 100
        insights.append(f"🏬 **สาขาที่มียอดขายสูงสุด:** สาขา **{best_branch}** ครองยอดขายอันดับ 1 ที่ **฿{best_branch_sales:,.2f}** ({best_branch_pct:.1f}% ของยอดขายรวม)")

    # 3. Best-Selling Product Insight
    top_prod_df = get_top_products(df, top_n=1)
    if not top_prod_df.empty:
        best_prod = top_prod_df.iloc[0]['product_name']
        best_prod_sales = top_prod_df.iloc[0]['net_sales']
        insights.append(f"🥧 **เมนูขายดีเด่น:** **{best_prod}** เป็นสินค้าที่ทำรายได้สูงสุด รวม **฿{best_prod_sales:,.2f}** แนะนำให้เตรียมวัตถุดิบและจัดโปรโมชันส่งเสริมการขายต่อเนื่อง")

    # 4. Payment Method Insight
    payment_df = get_sales_by_payment(df)
    if not payment_df.empty:
        top_pay = payment_df.iloc[0]['payment_method']
        top_pay_pct = (payment_df.iloc[0]['net_sales'] / total_sales) * 100
        insights.append(f"💳 **ช่องทางชำระเงินหลัก:** ลูกค้านิยมชำระเงินผ่าน **{top_pay}** มากที่สุด คิดเป็น **{top_pay_pct:.1f}%** ควรดูแลระบบรับชำระช่องทางนี้ให้ราบรื่นเสมอ")

    return insights

