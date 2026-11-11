# SQL analysis (SQLite)

This folder contains SQL queries for the IPL Auction Analysis project.

## Run it

From the project root in PowerShell:

```powershell
python load_sqlite.py
```

This creates `ipl_auction_analysis.db` and loads the three existing CSV datasets into SQLite tables. Then:

1. Open `ipl_auction_analysis.db` in **DB Browser for SQLite**.
2. Select **Execute SQL**.
3. Open `sql/01_analysis_queries.sql`, paste its contents into the SQL editor, and run the queries.

The queries cover season validation, duplicate checks, role-wise value-for-money ranking, relative low/high value, season comparison, a three-player watchlist and data-quality checks.

See `02_data_dictionary.md` for table definitions and metric interpretation.
