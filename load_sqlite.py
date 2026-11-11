"""Load project CSV outputs into a local SQLite database for SQL analysis."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "ipl_auction_analysis.db"
TABLE_FILES = {
    "auction_players": ROOT / "data" / "ipl_auction.csv",
    "seasonal_performance": ROOT / "data" / "clean" / "ipl_seasonal_performance.csv",
    "season_comparison": ROOT / "data" / "clean" / "player_season_comparison.csv",
}


def main():
    with sqlite3.connect(DB_PATH) as conn:
        for table, csv_path in TABLE_FILES.items():
            if not csv_path.exists():
                raise FileNotFoundError(f"Required CSV not found: {csv_path}")
            df = pd.read_csv(csv_path)
            if table == "auction_players":
                df = df.drop_duplicates()
            df.to_sql(table, conn, if_exists="replace", index=False)
            print(f"Loaded {table}: {len(df)} rows from {csv_path.relative_to(ROOT)}")

        # Basic SQL validation report
        print("\nSeason coverage:")
        report = pd.read_sql_query(
            "SELECT Season, COUNT(*) AS player_rows, "
            "COUNT(DISTINCT Player) AS unique_players "
            "FROM seasonal_performance GROUP BY Season ORDER BY Season",
            conn,
        )
        print(report.to_string(index=False))

    print(f"\nSQLite database created: {DB_PATH.name}")
    print("Open it in DB Browser for SQLite and run sql/01_analysis_queries.sql")


if __name__ == "__main__":
    main()
