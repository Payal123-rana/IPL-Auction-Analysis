# IPL Auction Analysis — Who Was Overpaid?

A data analytics project that compares selected players' IPL performance with their 2025 auction prices to identify relative value for money and build a performance-based watchlist.

## Business question

Which selected players delivered more batting or bowling output relative to their 2025 auction price, and which players could be monitored for a future auction?

## Tools

- Python, Pandas — JSON processing, cleaning, player-name matching and metric calculations
- SQL (SQLite) — validation, role-wise ranking, season comparison and target shortlist queries
- Streamlit, Plotly — interactive dashboard

## Project structure

```text
IPL_Auction_Analysis/
├── app.py
├── process_seasonal_data.py
├── calculate_value.py
├── compare_seasons.py
├── validate_project.py
├── process_ipl_data.py              # legacy all-season aggregation
├── merge_data.py                    # optional all-time career merge (19/19 names mapped)
├── FINAL_SUBMISSION_CHECKLIST.md
├── load_sqlite.py
├── requirements.txt
├── README.md
├── PROJECT_INSIGHTS.md
├── PROJECT_INSIGHTS.pdf
├── PROJECT_AUDIT.md
├── VIDEO_WALKTHROUGH_SCRIPT.md
├── sql/
│   ├── 01_analysis_queries.sql
│   ├── 02_data_dictionary.md
│   └── README.md
└── data/
    ├── ipl_auction.csv
    ├── SOURCES.md
    ├── raw/                          # Cricsheet JSON source matches
    └── clean/                        # processed CSV outputs
```

## How to run the project

Use Python 3.10 or later. Open PowerShell in the project root.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the full, reproducible pipeline and its checks:

```powershell
python validate_project.py
```

The validation script runs the seasonal pipeline, role-wise rankings, season comparison, optional all-time career aggregation and merge, SQLite loader, and all 10 SQL analysis queries. It stops if a required check fails. You can also run the individual scripts in the order shown in `validate_project.py`.

Run the dashboard:

```powershell
streamlit run app.py
```

## Run the SQL component

```powershell
python load_sqlite.py
```

This creates `ipl_auction_analysis.db` from the project's existing CSV files. Open that database in DB Browser for SQLite, choose **Execute SQL**, and run `sql/01_analysis_queries.sql`.

## Metric definitions

- **Batter / wicketkeeper:** runs per crore = season runs ÷ 2025 sold price (₹ crore).
- **Bowler:** bowler-credited wickets per crore = wickets ÷ 2025 sold price (₹ crore). Economy rate is supporting context; lower is better.
- **All-rounder:** runs per crore and wickets per crore are reported separately, avoiding an arbitrary weighted score.
- **Season comparison:** raw runs and wickets in 2025 vs 2026; it is not an auction-price comparison.
- **Two-season relative-value view:** 2025 and 2026 performance are each divided by the player's 2025 auction sold price. The 2026 result is a reference benchmark only, not a 2026 auction valuation.

## Data and interpretation caveats

- The cleaned auction CSV contains 19 unique selected players. One duplicate Phil Salt row in the supplied source file was removed.
- Cricsheet source archive contains 1,243 IPL match JSON files. The seasonal script filters the source to 2025 and 2026: 74 matches in each season (148 total).
- The processed sample has 19 selected players in each season (38 player-season rows); it is not a complete league-wide player ranking.
- The listed sold price is from the 2025 auction. It is carried beside 2026 performance for reference only and must not be described as a 2026 auction price.
- The lowest runs/wickets per crore is only the lowest relative value in this selected sample. It does not prove objective overpayment. Playing time, role, injuries, team environment, match conditions and auction demand are not fully modelled.
- The future-auction shortlist is an illustrative performance-based watchlist, not confirmation that the players will be available.

## Data source and attribution

Ball-by-ball match data: [Cricsheet IPL JSON downloads](https://cricsheet.org/downloads/). Auction-price reference links are listed in [`data/SOURCES.md`](data/SOURCES.md). Retain Cricsheet's `LICENSE.txt` and `README.txt` when redistributing the raw data.
<img width="1296" height="569" alt="Screenshot 2026-11-12 152635" src="https://github.com/user-attachments/assets/ed90a733-35a0-4843-a18f-35679da945e1" />
<img width="1040" height="459" alt="Screenshot 2026-11-12 152758" src="https://github.com/user-attachments/assets/e0edc2ed-94ee-4770-b150-4faf3b002605" />
<img width="1028" height="482" alt="Screenshot 2026-11-12 152824" src="https://github.com/user-attachments/assets/d5706216-317c-4078-87a6-0fa2244a7cd4" />
<img width="1007" height="411" alt="Screenshot 2026-11-12 152842" src="https://github.com/user-attachments/assets/4d6a278f-ff87-4198-94e2-6bbb6a2bb561" />




