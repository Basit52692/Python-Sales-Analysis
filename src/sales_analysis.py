"""End-to-end retail sales analysis pipeline.

Run from the project root:
    python run_analysis.py
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def load_data(path: str | Path) -> pd.DataFrame:
    """Load the raw sales CSV and parse date columns."""
    return pd.read_csv(path, parse_dates=["order_date", "ship_date"])


def validate_data(df: pd.DataFrame) -> dict:
    """Return core data-quality checks without silently dropping issues."""
    return {
        "rows": len(df),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "ship_before_order": int((df["ship_date"] < df["order_date"]).sum()),
        "negative_profit_orders": int((df["profit"] < 0).sum()),
        "unique_order_ids": int(df["order_id"].nunique()),
        "unique_customer_ids": int(df["customer_id"].nunique()),
        "unique_product_ids": int(df["product_id"].nunique()),
    }


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean duplicate rows and add analysis-ready features."""
    out = df.drop_duplicates().copy()
    out["order_year"] = out["order_date"].dt.year
    out["order_month"] = out["order_date"].dt.to_period("M").astype(str)
    out["month_name"] = out["order_date"].dt.month_name()
    out["shipping_days"] = (out["ship_date"] - out["order_date"]).dt.days
    out["discount_band"] = pd.cut(
        out["discount"],
        bins=[-0.001, 0, 0.1, 0.2, 1.0],
        labels=["0%", "1-10%", "11-20%", "20%+"],
        include_lowest=True,
    )
    out["profit_status"] = np.where(out["profit"] < 0, "Loss", "Profit")
    return out


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculate portfolio-level KPIs using aggregate-safe formulas."""
    total_sales = df["sales"].sum()
    total_profit = df["profit"].sum()
    return {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "profit_margin_pct": round(total_profit / total_sales * 100, 2),
        "orders": len(df),
        "units_sold": int(df["quantity"].sum()),
        "average_order_value": round(total_sales / len(df), 2),
        "average_shipping_days": round(df["shipping_days"].mean(), 2),
    }


def build_summary_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build reusable analytical tables for reporting."""
    yearly = df.groupby("order_year", as_index=False).agg(
        sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "count")
    )
    yearly["profit_margin_pct"] = yearly["profit"] / yearly["sales"] * 100
    yearly["yoy_sales_growth_pct"] = yearly["sales"].pct_change() * 100

    category = df.groupby("category", as_index=False).agg(
        sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "count")
    )
    category["profit_margin_pct"] = category["profit"] / category["sales"] * 100

    region = df.groupby("region", as_index=False).agg(
        sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "count")
    )
    region["profit_margin_pct"] = region["profit"] / region["sales"] * 100

    discount = df.groupby("discount", as_index=False).agg(
        sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "count")
    )
    discount["profit_margin_pct"] = discount["profit"] / discount["sales"] * 100

    return {"yearly": yearly, "category": category, "region": region, "discount": discount}


def save_outputs(df: pd.DataFrame, tables: dict[str, pd.DataFrame], output_dir: str | Path) -> None:
    """Export processed data, summary tables and four presentation charts."""
    output_dir = Path(output_dir)
    tables_dir = output_dir / "tables"
    charts_dir = output_dir / "charts"
    tables_dir.mkdir(parents=True, exist_ok=True)
    charts_dir.mkdir(parents=True, exist_ok=True)

    output_names = {
        "yearly": "yearly_performance.csv",
        "category": "category_performance.csv",
        "region": "region_performance.csv",
        "discount": "discount_analysis.csv",
    }
    for name, table in tables.items():
        table.to_csv(tables_dir / output_names[name], index=False)

    yearly = tables["yearly"].sort_values("order_year")
    plt.figure(figsize=(9, 5))
    plt.plot(yearly["order_year"], yearly["sales"], marker="o")
    plt.title("Annual Sales Trend")
    plt.xlabel("Year")
    plt.ylabel("Sales (source units)")
    plt.xticks(yearly["order_year"])
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1_000_000:.2f}M"))
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(charts_dir / "annual_sales_trend.png", dpi=180)
    plt.close()

    category = tables["category"].sort_values("sales", ascending=False)
    plt.figure(figsize=(9, 5))
    plt.bar(category["category"], category["sales"])
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales (source units)")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1_000_000:.2f}M"))
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(charts_dir / "sales_by_category.png", dpi=180)
    plt.close()

    region = tables["region"].sort_values("profit_margin_pct", ascending=False)
    plt.figure(figsize=(9, 5))
    plt.bar(region["region"], region["profit_margin_pct"])
    plt.title("Profit Margin by Region")
    plt.xlabel("Region")
    plt.ylabel("Profit Margin (%)")
    plt.tight_layout()
    plt.savefig(charts_dir / "margin_by_region.png", dpi=180)
    plt.close()

    discount = tables["discount"].sort_values("discount")
    plt.figure(figsize=(9, 5))
    plt.plot(discount["discount"] * 100, discount["profit_margin_pct"], marker="o")
    plt.title("Discount Level vs Profit Margin")
    plt.xlabel("Discount (%)")
    plt.xticks(discount["discount"] * 100, [f"{int(x)}%" for x in discount["discount"] * 100])
    plt.ylabel("Profit Margin (%)")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(charts_dir / "discount_vs_margin.png", dpi=180)
    plt.close()
