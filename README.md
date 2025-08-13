# DEMAND FORECASTING & OPTIMIZATION ON DATABRICKS (PySpark + FastAPI + Jenkins)

A practical, end-to-end case-study system that ingests raw sales/events, produces forecasts, and runs an inventory (or price) optimization - wired together with CI/CD (Jenkins) and a small REST layer to trigger/inspect runs. It shows you can design, implement, deploy, and reason about performance.

Given daily sales by product and store, this project aims to forecast the next 14-28 days. We can use these forecasts to optimize reorder quantities (or dynamic price buckets) under budget and service-level constraints.

