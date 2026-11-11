# SQL data dictionary

The SQLite database is created from the project's existing CSV outputs by `load_sqlite.py`.

| Table | Source file | Grain | Purpose |
|---|---|---|---|
| `auction_players` | `data/ipl_auction.csv` | One row per auction-list entry | 2025 auction price, team, role and country |
| `seasonal_performance` | `data/clean/ipl_seasonal_performance.csv` | One row per player per season | Runs, balls, wickets, economy and auction attributes |
| `season_comparison` | `data/clean/player_season_comparison.csv` | One row per selected player | 2025 vs 2026 changes |

## Important interpretation

- `Sold Price` is the 2025 auction price in this project. It is repeated beside the player's 2026 performance only as a reference price; it is **not** a 2026 auction price.
- Batter / wicketkeeper value is measured as runs per crore.
- Bowler value is measured as bowler-credited wickets per crore; economy is supporting context.
- All-rounder batting and bowling metrics are kept separate; no arbitrary combined score is created.
- The selected auction list contains 19 unique players. Rankings describe this sample only.
- The lowest value in a sample is not automatically proof that a player was objectively overpaid. Playing time, role, availability, team conditions and auction demand also matter.
- The 2026 relative-value query uses 2025 auction prices as a fixed benchmark because no 2026 auction price is present in this dataset.
