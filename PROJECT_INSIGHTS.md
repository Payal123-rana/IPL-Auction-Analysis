# IPL Auction Analysis — One-page Insight Memo

**Business question:** Which players in the selected 2025 auction sample delivered the strongest and weakest performance relative to their auction price, and who should be monitored for a future auction?

## Three numerical insights

1. **Batter value:** KL Rahul scored 546 runs at a 2025 sold price of ₹14 crore, equal to **39.00 runs per crore** — the highest in the selected batter/wicketkeeper sample. Rishabh Pant scored 269 runs at ₹27 crore, or **9.96 runs per crore**, the lowest in that sample.
2. **Bowler value:** Trent Boult took 22 wickets at ₹12.5 crore, equal to **1.76 wickets per crore** — the highest in the selected bowler sample. T. Natarajan took 1 wicket at ₹10.75 crore, or **0.09 wickets per crore**, the lowest in that sample. Economy rate should be reviewed alongside wickets.
3. **Year-on-year movement and benchmark:** Ishan Kishan's runs increased from 354 in 2025 to 602 in 2026 (**+248 runs**), while Bhuvneshwar Kumar's wickets increased from 17 to 28 (**+11 wickets**). With 2025 auction prices held constant as a reference, Ishan Kishan recorded **53.51 runs per crore** and Kagiso Rabada **2.70 wickets per crore** in 2026; these are not 2026 auction-price comparisons.

## Recommendation

For a performance-based future-auction watchlist from this dataset, monitor **Ishan Kishan** (602 runs in 2026), **Kagiso Rabada** (29 wickets in 2026), and **Marcus Stoinis** (216 runs and 2 wickets in 2026). These are role-based statistical candidates only; check availability, fitness, role fit, expected price and team requirements before making a bid decision.

## Method and limitations

Cricsheet ball-by-ball JSON was filtered to 2025 and 2026 and aggregated by player and season. Player names were mapped to the auction list before joining. Python/Pandas calculates the metrics; SQLite SQL independently provides ranking, comparison and validation queries; Streamlit/Plotly presents the dashboard.

The analysis covers 19 selected auction players, not every IPL player. Auction prices refer to the 2025 auction and are not 2026 prices. Runs/wickets per crore are simple output-to-price ratios and do not adjust for matches played, batting position, overs bowled, injury, role, team context or auction demand. Therefore, “lowest relative value” is only a screening signal and should not be interpreted as proof that a player was objectively overpaid. The auction spend shown in the dashboard is the spend of this selected sample, not the league-wide auction spend.

*Figures above are taken from the project's processed CSV outputs and were reproduced by rerunning the seasonal processing and ranking scripts in the supplied archive.*
