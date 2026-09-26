# Data Dictionary

| Column | Description |
|---|---|
| order_id | Transaction/order identifier |
| order_date | Date the order was placed |
| ship_date | Date the order was shipped |
| ship_mode | Shipping service level |
| customer_id | Customer identifier (unique per row in this practice dataset) |
| customer_name | Customer label |
| segment | Consumer, Corporate or Home Office |
| country | Country |
| city | City |
| state | State |
| postal_code | Postal code |
| region | Central, East or West |
| product_id | Product identifier (unique per row in this practice dataset) |
| category | High-level product category |
| sub_category | Product sub-category |
| product_name | Product label |
| sales | Sales amount in undocumented source currency/units |
| quantity | Units sold |
| discount | Discount rate as decimal |
| profit | Profit amount |
| order_year | Derived year |
| order_month | Derived YYYY-MM period |
| month_name | Derived month name |
| shipping_days | Derived ship date minus order date |
| discount_band | Derived discount bucket |
| profit_status | Profit or Loss classification |
| row_margin_pct | Row-level profit / sales percentage |
