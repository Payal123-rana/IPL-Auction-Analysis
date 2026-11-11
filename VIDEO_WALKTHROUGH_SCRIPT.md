# 2-minute project walkthrough script

**0:00–0:15 | Introduction**  
Hello, I am Payal. This is my IPL Auction Analysis project. The business question is: who delivered better value for money at the 2025 IPL auction, and which players should franchises monitor for a future auction?

**0:15–0:35 | Data and tools**  
I used Cricsheet ball-by-ball JSON data for the 2025 and 2026 seasons and a selected 2025 auction-price dataset. I used Python and Pandas for processing, SQL with SQLite for analysis and validation, and Streamlit with Plotly for the dashboard.

**0:35–1:05 | Method**  
First, I processed the JSON deliveries to calculate runs, balls faced, wickets, balls bowled, strike rate and economy. Then I mapped player names to the auction list and joined the performance with sold prices. For batters and wicketkeepers, I calculated runs per crore. For bowlers, I calculated wickets per crore and used economy as supporting context. For all-rounders, I kept batting and bowling value separate.

**1:05–1:35 | Key findings**  
In my selected sample, KL Rahul had the highest batter value at 39 runs per crore, while Rishabh Pant had the lowest at 9.96. Trent Boult led the bowler sample with 1.76 wickets per crore, while T. Natarajan had 0.09. I also compared 2025 and 2026 performance: Ishan Kishan improved by 248 runs, and Bhuvneshwar Kumar increased his wicket tally by 11.

**1:35–1:55 | Recommendation and limitations**  
Based on 2026 performance, my illustrative watchlist includes Ishan Kishan, Kagiso Rabada and Marcus Stoinis. These are not automatic buying recommendations. The analysis is limited to 19 selected players, and the 2025 auction price is not a 2026 price. Playing time, role and team context also affect performance.

**1:55–2:00 | Closing**  
Thank you. This project demonstrates my ability to clean and combine data, write SQL queries, calculate business metrics and communicate insights through a dashboard.
