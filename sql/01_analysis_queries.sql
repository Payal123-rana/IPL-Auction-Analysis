/* IPL AUCTION ANALYSIS — SQL ANALYSIS QUERIES
   Database: SQLite
   Tables are created/imported by load_sqlite.py.
   Note: Sold Price is the 2025 auction price. Do NOT treat it as a 2026 auction price.
*/

-- 1. Check the imported data and season coverage
SELECT Season, COUNT(*) AS player_records,
       COUNT(DISTINCT Player) AS unique_players
FROM seasonal_performance
GROUP BY Season
ORDER BY Season;

-- 2. Check whether a player appears more than once in a season
SELECT Season, Player, COUNT(*) AS duplicate_count
FROM seasonal_performance
GROUP BY Season, Player
HAVING COUNT(*) > 1;

-- 3. Batter / wicketkeeper value for money (2025 only)
-- Metric: runs scored per crore of 2025 auction price.
SELECT Player, Team, Role, Runs, "Sold Price" AS sold_price_crore,
       ROUND(Runs / NULLIF("Sold Price", 0), 2) AS runs_per_crore,
       RANK() OVER (
           ORDER BY Runs * 1.0 / NULLIF("Sold Price", 0) DESC
       ) AS value_rank
FROM seasonal_performance
WHERE Season = 2025
  AND Role IN ('Batsman', 'Wicketkeeper')
  AND "Sold Price" > 0
ORDER BY value_rank, Player;

-- 4. Bowler value for money (2025 only)
-- Metric: bowler-credited wickets per crore; economy is supporting context.
SELECT Player, Team, Wickets, "Sold Price" AS sold_price_crore,
       ROUND(Wickets * 1.0 / NULLIF("Sold Price", 0), 2) AS wickets_per_crore,
       Economy,
       RANK() OVER (
           ORDER BY Wickets * 1.0 / NULLIF("Sold Price", 0) DESC
       ) AS value_rank
FROM seasonal_performance
WHERE Season = 2025
  AND Role = 'Bowler'
  AND "Sold Price" > 0
ORDER BY value_rank, Player;

-- 5. All-rounders: keep batting and bowling value separate (2025 only)
SELECT Player, Team, Runs, Wickets,
       "Sold Price" AS sold_price_crore,
       ROUND(Runs * 1.0 / NULLIF("Sold Price", 0), 2) AS runs_per_crore,
       ROUND(Wickets * 1.0 / NULLIF("Sold Price", 0), 2) AS wickets_per_crore
FROM seasonal_performance
WHERE Season = 2025
  AND Role = 'All-Rounder'
  AND "Sold Price" > 0
ORDER BY runs_per_crore DESC, wickets_per_crore DESC;

-- 6. Relative lowest/highest value by role in BOTH seasons.
-- Sold Price remains the 2025 auction price in 2026; this is a benchmark only.
-- Lowest/highest are relative positions in this selected sample, not proof of over/underpayment.
WITH role_value AS (
    SELECT Season, Player, Role, Runs, Wickets, "Sold Price" AS sold_price_crore,
           CASE
             WHEN Role IN ('Batsman', 'Wicketkeeper')
               THEN Runs * 1.0 / NULLIF("Sold Price", 0)
             WHEN Role = 'Bowler'
               THEN Wickets * 1.0 / NULLIF("Sold Price", 0)
             ELSE NULL
           END AS role_value_metric,
           CASE
             WHEN Role IN ('Batsman', 'Wicketkeeper') THEN 'Runs per crore'
             WHEN Role = 'Bowler' THEN 'Wickets per crore'
             ELSE 'Separate all-rounder metrics'
           END AS metric_name
    FROM seasonal_performance
    WHERE Season IN (2025, 2026) AND "Sold Price" > 0
      AND Role IN ('Batsman', 'Wicketkeeper', 'Bowler')
), ranked AS (
    SELECT *,
           CASE WHEN Role IN ('Batsman', 'Wicketkeeper') THEN 'Batter' ELSE Role END AS role_group,
           RANK() OVER (PARTITION BY Season, CASE WHEN Role IN ('Batsman', 'Wicketkeeper') THEN 'Batter' ELSE Role END ORDER BY role_value_metric ASC) AS lowest_rank,
           RANK() OVER (PARTITION BY Season, CASE WHEN Role IN ('Batsman', 'Wicketkeeper') THEN 'Batter' ELSE Role END ORDER BY role_value_metric DESC) AS highest_rank
    FROM role_value
)
SELECT Season, Player, role_group, metric_name, role_value_metric,
       CASE WHEN lowest_rank = 1 THEN 'Lowest relative value'
            WHEN highest_rank = 1 THEN 'Highest relative value'
            ELSE 'Middle of sample' END AS relative_position
FROM ranked
WHERE lowest_rank = 1 OR highest_rank = 1
ORDER BY Season, role_group, relative_position;

-- 7. Season-over-season change for the selected players
SELECT Player, Runs_2025, Runs_2026, Runs_Change,
       Wickets_2025, Wickets_2026, Wickets_Change
FROM season_comparison
ORDER BY Runs_Change DESC;

-- 8. Top three performance-based next-auction watchlist (2026 stats)
-- One batter/wicketkeeper, one bowler and one all-rounder.
WITH candidates AS (
    SELECT *,
           ROW_NUMBER() OVER (
             PARTITION BY CASE WHEN Role IN ('Batsman', 'Wicketkeeper') THEN 'Batter' ELSE Role END
             ORDER BY
               CASE WHEN Role = 'Bowler' THEN Wickets ELSE Runs END DESC,
               CASE WHEN Role = 'All-Rounder' THEN Wickets ELSE 0 END DESC,
               Player
           ) AS role_rank
    FROM seasonal_performance
    WHERE Season = 2026
      AND Role IN ('Batsman', 'Wicketkeeper', 'Bowler', 'All-Rounder')
)
SELECT
    CASE WHEN Role IN ('Batsman', 'Wicketkeeper') THEN 'Batter'
         WHEN Role = 'Bowler' THEN 'Bowler'
         ELSE 'All-rounder' END AS target_category,
    Player, Team, Role, Runs, Wickets, Strike_Rate, Economy
FROM candidates
WHERE role_rank = 1
ORDER BY target_category;

-- 9. Auction-price consistency: confirm that each player has one listed price.
SELECT Player, COUNT(DISTINCT "Sold Price") AS distinct_prices,
       MIN("Sold Price") AS listed_sold_price_crore,
       COUNT(*) AS rows_in_seasonal_table
FROM seasonal_performance
GROUP BY Player
HAVING COUNT(DISTINCT "Sold Price") > 1;

-- 10. Null / zero denominator checks for value calculations
SELECT
    SUM(CASE WHEN "Sold Price" IS NULL OR "Sold Price" <= 0 THEN 1 ELSE 0 END) AS invalid_sold_price_rows,
    SUM(CASE WHEN Runs IS NULL THEN 1 ELSE 0 END) AS null_run_rows,
    SUM(CASE WHEN Wickets IS NULL THEN 1 ELSE 0 END) AS null_wicket_rows
FROM seasonal_performance;
