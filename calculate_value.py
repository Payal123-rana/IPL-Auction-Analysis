
import pandas as pd
import os

# Load seasonal performance data
df = pd.read_csv("data/clean/ipl_seasonal_performance.csv")

# First calculate rankings for 2025 only,
# because Sold Price in this dataset is from the 2025 auction.
df = df[df["Season"] == 2025].copy()

# Remove rows with invalid auction prices
df = df[df["Sold Price"] > 0].copy()

# Calculate role-specific value metrics
df["Runs_Per_Crore"] = (
    df["Runs"] / df["Sold Price"]
)

df["Wickets_Per_Crore"] = (
    df["Wickets"] / df["Sold Price"]
)

# Create output folder
os.makedirs("data/clean", exist_ok=True)

# Batter and wicketkeeper ranking
batters = df[
    df["Role"].isin(["Batsman", "Wicketkeeper"])
].copy()

batters = batters.sort_values(
    "Runs_Per_Crore", ascending=False
)

batters["Value_Rank"] = range(1, len(batters) + 1)

batters.to_csv(
    "data/clean/batter_value_ranking.csv",
    index=False
)

# Bowler ranking
bowlers = df[df["Role"] == "Bowler"].copy()

bowlers = bowlers.sort_values(
    "Wickets_Per_Crore", ascending=False
)

bowlers["Value_Rank"] = range(1, len(bowlers) + 1)

bowlers.to_csv(
    "data/clean/bowler_value_ranking.csv",
    index=False
)

# All-rounder ranking
all_rounders = df[df["Role"] == "All-Rounder"].copy()

all_rounders = all_rounders.sort_values(
    ["Runs_Per_Crore", "Wickets_Per_Crore"],
    ascending=[False, False]
)

all_rounders["Value_Rank"] = range(
    1, len(all_rounders) + 1
)

all_rounders.to_csv(
    "data/clean/all_rounder_value_ranking.csv",
    index=False
)

print("========== VALUE FOR MONEY RANKING ==========")

print("\nTOP BATTERS:")
print(
    batters[["Player", "Runs", "Sold Price", "Runs_Per_Crore"]]
    .head(5).to_string(index=False)
)

print("\nTOP BOWLERS:")
print(
    bowlers[["Player", "Wickets", "Sold Price",
             "Wickets_Per_Crore", "Economy"]]
    .head(5).to_string(index=False)
)

print("\nALL-ROUNDERS:")
print(
    all_rounders[["Player", "Runs", "Wickets",
                  "Sold Price", "Runs_Per_Crore",
                  "Wickets_Per_Crore"]]
    .to_string(index=False)
)

print("\nRanking files saved successfully!")

# Two-season relative-value benchmark. The denominator remains the 2025
# auction sold price in both seasons; 2026 is NOT a 2026 auction-price analysis.
all_seasons = pd.read_csv("data/clean/ipl_seasonal_performance.csv")
all_seasons = all_seasons[all_seasons["Sold Price"] > 0].copy()
all_seasons["Runs_Per_Crore"] = all_seasons["Runs"] / all_seasons["Sold Price"]
all_seasons["Wickets_Per_Crore"] = all_seasons["Wickets"] / all_seasons["Sold Price"]
all_seasons["Role_Group"] = all_seasons["Role"].map(
    lambda role: "Batter" if role in ["Batsman", "Wicketkeeper"] else role
)
all_seasons["Metric_Name"] = all_seasons["Role_Group"].map({
    "Batter": "Runs per crore (2025 auction price)",
    "Bowler": "Wickets per crore (2025 auction price)",
    "All-Rounder": "Separate batting and bowling metrics"
})
all_seasons["Role_Metric"] = all_seasons.apply(
    lambda row: row["Runs_Per_Crore"] if row["Role_Group"] == "Batter"
    else (row["Wickets_Per_Crore"] if row["Role_Group"] == "Bowler" else float("nan")),
    axis=1
)
rankable = all_seasons[all_seasons["Role_Group"].isin(["Batter", "Bowler"])].copy()
rankable["Value_Rank"] = rankable.groupby(["Season", "Role_Group"])["Role_Metric"].rank(
    method="min", ascending=False
).astype(int)
rankable["Lowest_Value_Rank"] = rankable.groupby(["Season", "Role_Group"])["Role_Metric"].rank(
    method="min", ascending=True
).astype(int)
rankable.to_csv("data/clean/season_role_value_ranking.csv", index=False)
print("Two-season role-wise relative-value benchmark saved:")
print("data/clean/season_role_value_ranking.csv")
