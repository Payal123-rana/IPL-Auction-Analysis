
import json
import glob
import os
import pandas as pd
from collections import defaultdict

# -----------------------------
# CONFIGURATION
# -----------------------------

SEASONS = ["2025", "2026"]

PLAYER_MAPPING = {
    "Rishabh Pant": "RR Pant",
    "Shreyas Iyer": "SS Iyer",
    "Venkatesh Iyer": "VR Iyer",
    "Arshdeep Singh": "Arshdeep Singh",
    "Yuzvendra Chahal": "YS Chahal",
    "Jos Buttler": "JC Buttler",
    "KL Rahul": "KL Rahul",
    "Trent Boult": "TA Boult",
    "Jofra Archer": "JC Archer",
    "Phil Salt": "PD Salt",
    "Mohammed Siraj": "Mohammed Siraj",
    "Mitchell Starc": "MA Starc",
    "Ishan Kishan": "Ishan Kishan",
    "Jitesh Sharma": "JM Sharma",
    "Marcus Stoinis": "MP Stoinis",
    "Bhuvneshwar Kumar": "B Kumar",
    "Kagiso Rabada": "K Rabada",
    "T. Natarajan": "T Natarajan",
    "Mohammed Shami": "Mohammed Shami"
}

BOWLER_WICKET_TYPES = {
    "bowled",
    "caught",
    "caught and bowled",
    "lbw",
    "stumped",
    "hit wicket"
}

# -----------------------------
# LOAD AUCTION DATA
# -----------------------------

auction = pd.read_csv("data/ipl_auction.csv")

# Remove only exact duplicate records
auction = auction.drop_duplicates()

auction["Player_Performance"] = auction["Player"].map(
    PLAYER_MAPPING
)

# -----------------------------
# SEASON-WISE PERFORMANCE
# -----------------------------

stats = defaultdict(
    lambda: {
        "Runs": 0,
        "Balls_Faced": 0,
        "Wickets": 0,
        "Balls_Bowled": 0,
        "Runs_Conceded": 0
    }
)

files = glob.glob("data/raw/*.json")

processed_matches = 0

for file in files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    info = match.get("info", {})
    season = str(info.get("season"))

    if season not in SEASONS:
        continue

    processed_matches += 1

    for innings in match.get("innings", []):

        for over in innings.get("overs", []):

            for delivery in over.get("deliveries", []):

                batter = delivery.get("batter")
                bowler = delivery.get("bowler")

                runs = delivery.get("runs", {})
                extras = delivery.get("extras", {})

                batter_runs = runs.get("batter", 0)
                total_runs = runs.get("total", 0)

                wides = extras.get("wides", 0)
                noballs = extras.get("noballs", 0)

                byes = extras.get("byes", 0)
                legbyes = extras.get("legbyes", 0)
                penalty = extras.get("penalty", 0)

                # BATTING STATS

                stats[(season, batter)]["Runs"] += batter_runs

                # Wide deliveries do not count as balls faced
                if wides == 0:
                    stats[(season, batter)]["Balls_Faced"] += 1

                # BOWLING STATS

                # Wides and no-balls are not legal balls
                if wides == 0 and noballs == 0:
                    stats[(season, bowler)]["Balls_Bowled"] += 1

                # Exclude byes, legbyes and penalty from bowler runs
                bowler_runs = (
                    total_runs - byes - legbyes - penalty
                )

                stats[(season, bowler)]["Runs_Conceded"] += bowler_runs

                # Count only wickets credited to the bowler
                for wicket in delivery.get("wickets", []):

                    if wicket.get("kind") in BOWLER_WICKET_TYPES:
                        stats[(season, bowler)]["Wickets"] += 1

# -----------------------------
# CREATE SEASONAL DATAFRAME
# -----------------------------

rows = []

for (season, player), values in stats.items():

    auction_players = set(PLAYER_MAPPING.values())

    if player not in auction_players:
        continue

    balls_faced = values["Balls_Faced"]
    balls_bowled = values["Balls_Bowled"]

    strike_rate = (
        round(values["Runs"] * 100 / balls_faced, 2)
        if balls_faced > 0 else None
    )

    economy = (
        round(values["Runs_Conceded"] * 6 / balls_bowled, 2)
        if balls_bowled > 0 else None
    )

    rows.append({
        "Season": season,
        "Player_Performance": player,
        "Runs": values["Runs"],
        "Balls_Faced": balls_faced,
        "Wickets": values["Wickets"],
        "Balls_Bowled": balls_bowled,
        "Runs_Conceded": values["Runs_Conceded"],
        "Strike_Rate": strike_rate,
        "Economy": economy
    })

seasonal_df = pd.DataFrame(rows)

# -----------------------------
# MATCH WITH AUCTION DATA
# -----------------------------

final_df = seasonal_df.merge(
    auction,
    on="Player_Performance",
    how="left"
)

# Arrange columns
columns = [
    "Season",
    "Player",
    "Team",
    "Role",
    "Country",
    "Base Price",
    "Sold Price",
    "Player_Performance",
    "Runs",
    "Balls_Faced",
    "Wickets",
    "Balls_Bowled",
    "Runs_Conceded",
    "Strike_Rate",
    "Economy"
]

final_df = final_df[columns]

# -----------------------------
# SAVE OUTPUT
# -----------------------------

os.makedirs("data/clean", exist_ok=True)

output_file = "data/clean/ipl_seasonal_performance.csv"

final_df.to_csv(output_file, index=False)

print("\n========== SEASONAL PROCESSING REPORT ==========")

print("Total JSON Files:", len(files))
print("2025 and 2026 Matches Processed:", processed_matches)

print("\nSeason-wise Player Record Count:")
print(
    final_df.groupby("Season")["Player"].count()
)

print("\nTotal Seasonal Player Records:", len(final_df))

print("\nOutput Saved:", output_file)

print("\nPlayer-wise Seasonal Performance:")
print(final_df.to_string(index=False))
