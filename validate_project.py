"""Run the complete IPL auction analysis pipeline and validate its outputs."""
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "process_seasonal_data.py",
    "calculate_value.py",
    "compare_seasons.py",
    "process_ipl_data.py",
    "merge_data.py",
    "load_sqlite.py",
]


def run_script(name: str) -> None:
    print(f"\n{'=' * 18} RUNNING {name} {'=' * 18}")
    subprocess.run([sys.executable, name], cwd=ROOT, check=True)


def sql_statements(path: Path):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"--.*?$", "", text, flags=re.M)
    buffer = ""
    for line in text.splitlines():
        buffer += line + "\n"
        if sqlite3.complete_statement(buffer):
            statement = buffer.strip()
            if statement:
                yield statement
            buffer = ""
    if buffer.strip():
        raise ValueError("Unterminated SQL statement in analysis query file")


def main():
    raw_files = list((ROOT / "data" / "raw").glob("*.json"))
    if not raw_files:
        raise FileNotFoundError("No Cricsheet JSON files found in data/raw")

    for script in SCRIPTS:
        run_script(script)

    seasonal_path = ROOT / "data/clean/ipl_seasonal_performance.csv"
    comparison_path = ROOT / "data/clean/player_season_comparison.csv"
    auction_path = ROOT / "data/ipl_auction.csv"
    seasonal = pd.read_csv(seasonal_path)
    comparison = pd.read_csv(comparison_path)
    auction = pd.read_csv(auction_path)
    season_rankings = pd.read_csv(ROOT / "data/clean/season_role_value_ranking.csv")

    assert len(auction) == 19, f"Expected 19 unique auction rows, got {len(auction)}"
    assert not auction.duplicated().any(), "Auction CSV still contains duplicate rows"
    assert seasonal.groupby("Season").size().to_dict() == {2025: 19, 2026: 19}, \
        f"Unexpected season coverage: {seasonal.groupby('Season').size().to_dict()}"
    assert not seasonal.duplicated(["Season", "Player"]).any(), "Duplicate player-season rows found"
    assert seasonal[["Player", "Team", "Role", "Sold Price", "Runs", "Wickets"]].notna().all().all(), \
        "Required seasonal fields contain nulls"
    assert (seasonal["Sold Price"] > 0).all(), "Non-positive auction price found"
    assert len(comparison) == 19, f"Expected 19 player comparisons, got {len(comparison)}"
    assert (ROOT / "PROJECT_INSIGHTS.pdf").exists(), "One-page insight memo PDF is missing"
    assert set(season_rankings["Season"].unique()) == {2025, 2026}, "Two-season value ranking is incomplete"
    assert set(season_rankings["Role_Group"].unique()) == {"Batter", "Bowler"}, "Role-wise value ranking is incomplete"

    merged = pd.read_csv(ROOT / "data/clean/ipl_auction_career_performance.csv")
    assert len(merged) == 19, f"Legacy auction merge should have 19 rows, got {len(merged)}"
    assert merged["Runs"].notna().all(), "Legacy auction merge contains unmatched players"

    db_path = ROOT / "ipl_auction_analysis.db"
    query_path = ROOT / "sql/01_analysis_queries.sql"
    with sqlite3.connect(db_path) as conn:
        statements = list(sql_statements(query_path))
        results = []
        for number, statement in enumerate(statements, start=1):
            cursor = conn.execute(statement)
            rows = cursor.fetchall() if cursor.description else []
            results.append((number, len(rows)))
            if number == 8:
                targets = {row[0]: row[1] for row in rows}
                assert targets == {"All-rounder": "Marcus Stoinis", "Batter": "Ishan Kishan", "Bowler": "Kagiso Rabada"}, \
                    f"Unexpected SQL target shortlist: {targets}"
        assert len(statements) == 10, f"Expected 10 SQL queries, found {len(statements)}"

    print("\n========== FINAL VALIDATION ==========")
    print(f"Raw Cricsheet JSON files: {len(raw_files):,}")
    print("2025 player-season rows: 19")
    print("2026 player-season rows: 19")
    print("Auction players: 19 unique records")
    print("Season comparison rows: 19")
    print("Two-season role-wise relative value rankings: 2025 and 2026")
    print("Legacy career auction merge: 19/19 matched")
    print(f"SQL queries executed successfully: {len(results)}")
    print("SQL result row counts:", ", ".join(f"Q{n}={r}" for n, r in results))
    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
