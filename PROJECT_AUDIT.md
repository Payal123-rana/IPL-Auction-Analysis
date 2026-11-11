# Project audit and validation log

## Verified source and processing coverage

- Cricsheet JSON files in `data/raw/`: **1,243**.
- IPL matches filtered by season: **74 in 2025** and **74 in 2026**.
- Auction file after removing the exact duplicate Phil Salt row: **19 unique players**.
- Seasonal output: **38 player-season rows** (19 players in each season).
- Duplicate player-season keys: **0**.
- Required player, team, role, sold-price, runs and wickets fields: **no nulls**.
- Legacy all-time career merge: **19/19 auction players matched**.

## Code and SQL validation

Run `python validate_project.py` from the project root. The final run completed successfully:

- Seasonal processing, value rankings and season comparison regenerated.
- Optional all-time career aggregation and auction merge regenerated.
- SQLite database rebuilt from the cleaned CSV files.
- All **10 SQL analysis queries** executed successfully.
- SQL query 6 returns role-wise lowest/highest relative-value players separately for both seasons.
- SQL query 8 returns one 2026 target each for batter, bowler and all-rounder; the all-rounder selection logic matches the dashboard (runs first, wickets as tie-breaker).
- Python syntax compilation passed for all project scripts and dashboard source.

## Key findings reproduced from the processed CSVs

- 2025 batter/wicketkeeper sample: KL Rahul highest at **39.00 runs/crore**; Rishabh Pant lowest at **9.96 runs/crore**.
- 2025 bowler sample: Trent Boult highest at **1.76 wickets/crore**; T. Natarajan lowest at **0.09 wickets/crore**.
- 2026 performance benchmark using 2025 auction prices: Ishan Kishan highest batter ratio at **53.51 runs/crore**; Kagiso Rabada highest bowler ratio at **2.70 wickets/crore**.
- 2026 target shortlist: Ishan Kishan (602 runs), Kagiso Rabada (29 wickets), Marcus Stoinis (216 runs, 2 wickets).

## Interpretation limits

- The analysis covers a selected 19-player sample, not the full IPL auction or league.
- The price denominator is the 2025 auction sold price. It is repeated beside 2026 performance only as a fixed reference and is not a 2026 auction price.
- Runs/wickets per crore do not adjust for matches played, batting position, overs bowled, injury, role changes, team context or auction demand.
- Lowest relative value is a screening signal, not proof of objective overpayment.
- The future-auction shortlist is illustrative; availability, fitness, expected price and franchise role fit need separate research.

## Dashboard execution note

The dashboard source passed Python syntax compilation and its required CSV inputs were regenerated. Streamlit was not installed in the packaging environment and network access prevented installing it, so the interactive UI could not be launched here. On the user's Windows machine, install `requirements.txt` and run `streamlit run app.py`.
