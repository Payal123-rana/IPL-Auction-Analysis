
import pandas as pd
import os

# =====================================
# 1. FILE PATHS
# =====================================

AUCTION_FILE = "data/ipl_auction.csv"
PERFORMANCE_FILE = "data/clean/player_career_performance.csv"
OUTPUT_FOLDER = "data/clean"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =====================================
# 2. LOAD DATASETS
# =====================================

auction_df = pd.read_csv(AUCTION_FILE)
# Remove exact duplicate auction rows before joining (e.g. duplicate player records).
auction_df = auction_df.drop_duplicates()
performance_df = pd.read_csv(PERFORMANCE_FILE)

print("Auction Dataset:", auction_df.shape)
print("Performance Dataset:", performance_df.shape)

# =====================================
# 3. CLEAN PLAYER NAMES
# =====================================

auction_df["Player"] = (
    auction_df["Player"].astype(str).str.strip()
)

performance_df["Player"] = (
    performance_df["Player"].astype(str).str.strip()
)

# =====================================
# 4. PLAYER NAME MAPPING
# =====================================

player_mapping = {
    "Rishabh Pant": "RR Pant",
    "Shreyas Iyer": "SS Iyer",
    "Venkatesh Iyer": "VR Iyer",
    "Yuzvendra Chahal": "YS Chahal",
    "Jos Buttler": "JC Buttler",
    "Trent Boult": "TA Boult",
    "Jofra Archer": "JC Archer",
    "Phil Salt": "PD Salt",
    "Mitchell Starc": "MA Starc",
    "Marcus Stoinis": "MP Stoinis",
    "Kagiso Rabada": "K Rabada",
    "T. Natarajan": "T Natarajan",
    "Jitesh Sharma": "JM Sharma",
    "Bhuvneshwar Kumar": "B Kumar"
}

# =====================================
# 5. CREATE MATCHING KEY
# =====================================

auction_df["Merge_Player"] = (
    auction_df["Player"].replace(player_mapping)
)

performance_df["Merge_Player"] = (
    performance_df["Player"]
)

# =====================================
# 6. MERGE DATASETS
# =====================================

merged_df = pd.merge(
    auction_df,
    performance_df,
    on="Merge_Player",
    how="left",
    suffixes=("", "_Performance")
)

# Remove temporary column
merged_df.drop(
    columns=["Merge_Player"],
    inplace=True
)

# =====================================
# 7. SAVE FINAL DATASET
# =====================================

output_path = os.path.join(
    OUTPUT_FOLDER,
    "ipl_auction_career_performance.csv"
)

merged_df.to_csv(output_path, index=False)

# =====================================
# 8. MATCHING REPORT
# =====================================

matched = merged_df["Runs"].notna().sum()
unmatched = merged_df["Runs"].isna().sum()

print("\n========== MERGE REPORT ==========")

print("Total Auction Records:", len(auction_df))
print("Matched Records:", matched)
print("Unmatched Records:", unmatched)

print("\n========== UNMATCHED PLAYERS ==========")

unmatched_players = merged_df.loc[
    merged_df["Runs"].isna(), "Player"
]

print(unmatched_players.to_string(index=False))

# =====================================
# 9. DISPLAY TOP 10 RECORDS
# =====================================

print("\n========== TOP 10 RECORDS ==========")

print(
    merged_df.head(10).to_string(index=False)
)

print("\nFinal Dataset Saved Successfully!")
print("File Location:", output_path)

print("\n===================================")
