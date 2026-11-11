# Final submission checklist

| Requirement | Project file / section | Status |
|---|---|---|
| Raw ball-by-ball source data | `data/raw/` + Cricsheet attribution files | Included |
| Auction-price sample | `data/ipl_auction.csv` | 19 unique players; duplicate removed |
| Cleaning and player-name matching | `process_seasonal_data.py` | Included; 19/19 players matched |
| Batter value metric | `calculate_value.py`, dashboard, SQL query 3 | Runs per crore |
| Bowler value metric | `calculate_value.py`, dashboard, SQL query 4 | Wickets per crore; economy context |
| All-rounder treatment | ranking CSV, dashboard, SQL query 5 | Runs/crore and wickets/crore shown separately |
| Two-season comparison | `compare_seasons.py`, dashboard, SQL query 7 | 2025 vs 2026 runs and wickets |
| Two-season relative value view | `season_role_value_ranking.csv`, dashboard, SQL query 6 | 2025 price used as benchmark in both seasons; caveat displayed |
| Three target players | dashboard, `PROJECT_INSIGHTS.md`, SQL query 8 | Batter, bowler and all-rounder candidates |
| SQL analysis | `sql/01_analysis_queries.sql` | 10 queries; all execute successfully |
| Data dictionary and sources | `sql/02_data_dictionary.md`, `data/SOURCES.md` | Included |
| Reproducible validation | `validate_project.py` | Passed |
| Insight memo | `PROJECT_INSIGHTS.md`, `PROJECT_INSIGHTS.pdf` | Included (Markdown + one-page PDF) |
| 2-minute walkthrough script | `VIDEO_WALKTHROUGH_SCRIPT.md` | Included |
| Interactive dashboard | `app.py` | Code and data included; local launch still required |

## Important caveats

- The auction list is a 19-player sample, not all players sold at the 2025 auction.
- 2026 relative-value ratios use the 2025 sold price only as a fixed reference. They are not 2026 auction-value conclusions.
- Lowest value in this sample is a screening signal, not proof of overpayment.
- The dashboard was not launched in the packaging environment because Streamlit was unavailable there. Run it locally after installing `requirements.txt`.
