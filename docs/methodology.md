# Methodology

## 1. Ingestion
The source workbook Data sheet was exported to CSV so the project can be run without Excel dependencies.

## 2. Validation
The pipeline checks row count, duplicates, missing cells, invalid shipping chronology and loss-making orders. Loss-making orders are retained because they are analytically meaningful.

## 3. Feature engineering
Derived fields include order year, order month, shipping days, discount band and profit status.

## 4. KPI design
Profit margin is calculated as `SUM(profit) / SUM(sales)`, not the average of row-level margins. Average order value is `SUM(sales) / order count`.

## 5. Analysis
Grouped analysis covers year, month, category, region, discount and ship mode. `pct_change()` is used for year-over-year sales growth.

## 6. Interpretation guardrails
Discount-versus-margin results are descriptive associations. No causal claim is made. Currency is unspecified in the source and is therefore not invented.
