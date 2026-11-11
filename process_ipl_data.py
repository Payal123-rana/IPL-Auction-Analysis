
import json
import glob
import pandas as pd
import os

# =====================================
# PROJECT PATHS
# =====================================

RAW_FOLDER = "data/raw"
OUTPUT_FOLDER = "data/clean"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

player_stats = {}

# Only these dismissal types are credited to the bowler in cricket scorecards.
BOWLER_WICKET_TYPES = {
    "bowled", "caught", "caught and bowled", "lbw", "stumped", "hit wicket"
}

# =====================================
# READ ALL IPL JSON FILES
# =====================================

files = glob.glob(os.path.join(RAW_FOLDER, "*.json"))

print(f"Total matches found: {len(files)}")

for file in files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    for innings in match.get("innings", []):

        for over in innings.get("overs", []):

            for delivery in over.get("deliveries", []):

                batter = delivery["batter"]
                bowler = delivery["bowler"]

                batter_runs = delivery["runs"]["batter"]
                total_runs = delivery["runs"]["total"]

                extras = delivery.get("extras", {})

                # Wide and no-ball do not count as legal balls
                legal_ball = not any(
                    key in extras for key in ["wides", "noballs"]
                )

                # Initialize batter statistics
                if batter not in player_stats:

                    player_stats[batter] = {
                        "Player": batter,
                        "Runs": 0,
                        "Balls_Faced": 0,
                        "Wickets": 0,
                        "Balls_Bowled": 0,
                        "Runs_Conceded": 0
                    }

                # Initialize bowler statistics
                if bowler not in player_stats:

                    player_stats[bowler] = {
                        "Player": bowler,
                        "Runs": 0,
                        "Balls_Faced": 0,
                        "Wickets": 0,
                        "Balls_Bowled": 0,
                        "Runs_Conceded": 0
                    }

                # Batting runs
                player_stats[batter]["Runs"] += batter_runs

                # Bowling runs conceded
                # Byes, leg-byes and penalty runs are not charged to the bowler.
                bowler_runs = (
                    total_runs
                    - extras.get("byes", 0)
                    - extras.get("legbyes", 0)
                    - extras.get("penalty", 0)
                )
                player_stats[bowler]["Runs_Conceded"] += bowler_runs

                # Ball count
                if legal_ball:
                    player_stats[bowler]["Balls_Bowled"] += 1

                # Balls faced: exclude wides only
                if "wides" not in extras:
                    player_stats[batter]["Balls_Faced"] += 1

                # Wickets credited to bowler
                for wicket in delivery.get("wickets", []):

                    if wicket.get("kind") in BOWLER_WICKET_TYPES:
                        player_stats[bowler]["Wickets"] += 1

# =====================================
# CREATE DATAFRAME
# =====================================

df = pd.DataFrame(list(player_stats.values()))

# =====================================
# CALCULATE PERFORMANCE METRICS
# =====================================

df["Strike_Rate"] = (
    df["Runs"] /
    df["Balls_Faced"].replace(0, float("nan")) * 100
).round(2)

df["Economy"] = (
    df["Runs_Conceded"] /
    (df["Balls_Bowled"].replace(0, float("nan")) / 6)
).round(2)

# =====================================
# SAVE CLEAN DATASET
# =====================================

output_path = os.path.join(
    OUTPUT_FOLDER,
    "player_career_performance.csv"
)

df.to_csv(output_path, index=False)

# =====================================
# FINAL OUTPUT
# =====================================

print("\n=================================")
print("CAREER PERFORMANCE DATASET CREATED!")
print("=================================")

print("\nTOP 10 PLAYERS:")
print(df.head(10).to_string(index=False))

print(f"\nTotal Players: {len(df)}")

print(f"\nSaved File: {output_path}")

print("\nProcessing Completed Successfully!")
