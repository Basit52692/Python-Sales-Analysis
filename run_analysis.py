from pathlib import Path
import pandas as pd
from src.sales_analysis import load_data, validate_data, prepare_data, calculate_kpis, build_summary_tables, save_outputs

ROOT = Path(__file__).resolve().parent
RAW_FILE = ROOT / "data" / "raw" / "sales_orders.csv"
PROCESSED_FILE = ROOT / "data" / "processed" / "clean_sales_orders.csv"
OUTPUT_DIR = ROOT / "outputs"


def main():
    df = load_data(RAW_FILE)
    quality = validate_data(df)
    clean = prepare_data(df)
    kpis = calculate_kpis(clean)
    tables = build_summary_tables(clean)

    clean.to_csv(PROCESSED_FILE, index=False, date_format="%Y-%m-%d")
    save_outputs(clean, tables, OUTPUT_DIR)

    pd.DataFrame([quality]).to_csv(OUTPUT_DIR / "tables" / "data_quality_runtime.csv", index=False)
    pd.DataFrame([kpis]).to_csv(OUTPUT_DIR / "tables" / "kpi_runtime.csv", index=False)

    print("Analysis complete")
    print("Data quality:", quality)
    print("KPIs:", kpis)
    print(f"Processed data: {PROCESSED_FILE}")
    print(f"Outputs: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
