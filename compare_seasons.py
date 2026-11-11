
import pandas as pd

df = pd.read_csv("data/clean/ipl_seasonal_performance.csv")

comparison = df.pivot_table(
    index="Player",
    columns="Season",
    values=["Runs", "Wickets"],
    aggfunc="sum"
).fillna(0)

comparison.columns = [
    f"{metric}_{season}"
    for metric, season in comparison.columns
]

comparison = comparison.reset_index()

comparison["Runs_Change"] = (
    comparison["Runs_2026"] - comparison["Runs_2025"]
)

comparison["Wickets_Change"] = (
    comparison["Wickets_2026"] - comparison["Wickets_2025"]
)

comparison.to_csv(
    "data/clean/player_season_comparison.csv",
    index=False
)

print("========== SEASON COMPARISON ==========")

print(
    comparison[
        ["Player", "Runs_Change", "Wickets_Change"]
    ].to_string(index=False)
)

print("\nComparison file saved successfully!")
