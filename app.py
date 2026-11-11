
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="IPL Auction Analysis",
    page_icon="🏏",
    layout="wide"
)

# =====================================================
# THEME
# =====================================================
BG = "#06122E"

TEAM_COLORS = {
    "CSK": "#FFD21F", "MI": "#168BFF",
    "RCB": "#FF3B45", "KKR": "#9148E8",
    "SRH": "#FF791A", "RR": "#E83DA9",
    "DC": "#367DFF", "PBKS": "#F04444",
    "GT": "#13BFCB", "LSG": "#38C987"
}

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 75% 5%, #10285A 0%, transparent 28%),
                linear-gradient(135deg, #030B20, #07183B 55%, #06112B);
    color: white;
}

.block-container {
    max-width: 1800px;
    padding: 1rem 1.2rem 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06164B, #081C52 65%, #07112F);
    border-right: 1px solid #1B65C8;
}

[data-testid="stSidebar"] label {
    color: #EAF4FF !important;
    font-weight: 600;
}

[data-testid="stPlotlyChart"] {
    background: linear-gradient(145deg, #091B43, #071638);
    border: 1px solid #164EAA;
    border-radius: 15px;
    padding: 5px;
}

.section-title {
    font-size: 19px;
    font-weight: 800;
    color: white;
    padding: 10px 0;
}

.kpi-card {
    padding: 17px 12px;
    border-radius: 14px;
    min-height: 110px;
    box-shadow: 0 5px 18px #00000040;
}

.kpi-value {
    font-size: 25px;
    font-weight: 900;
    color: white;
}

.kpi-label {
    font-size: 13px;
    font-weight: 800;
    color: white;
}

.kpi-note {
    font-size: 11px;
    color: #E0EAFF;
    margin-top: 5px;
}

.insight-box {
    background: linear-gradient(100deg, #171044, #071B49);
    border: 1px solid #9C41E8;
    border-radius: 14px;
    padding: 15px;
}

div.stButton > button {
    background: linear-gradient(90deg, #087FC5, #6429C9);
    color: white;
    border: 1px solid #44D9FF;
    border-radius: 9px;
    font-weight: 700;
}

h1, h2, h3 {
    color: white !important;
}

hr {
    border-color: #17417C;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():

    performance = pd.read_csv(
        "data/clean/ipl_seasonal_performance.csv"
    )

    comparison = pd.read_csv(
        "data/clean/player_season_comparison.csv"
    )

    numeric_columns = [
        "Season", "Base Price", "Sold Price",
        "Runs", "Balls_Faced", "Wickets",
        "Balls_Bowled", "Runs_Conceded",
        "Strike_Rate", "Economy"
    ]

    for col in numeric_columns:
        if col in performance.columns:
            performance[col] = pd.to_numeric(
                performance[col], errors="coerce"
            )

    performance = performance.drop_duplicates(
        subset=["Season", "Player"]
    )

    return performance, comparison


try:
    original_df, comparison_df = load_data()

except Exception as error:
    st.error(f"Dataset loading error: {error}")
    st.info(
        "Please check that both CSV files exist inside data/clean."
    )
    st.stop()


# =====================================================
# 2025 AUCTION DATA
# =====================================================
auction_df = original_df[
    original_df["Season"] == 2025
].copy()

auction_df = auction_df.drop_duplicates(
    subset=["Player"]
)

if auction_df.empty:
    st.error("2025 auction data not found.")
    st.stop()


# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.markdown("""
<div style="text-align:center;padding:10px 0 20px;">
    <div style="font-size:55px;">🏏</div>
    <div style="font-size:29px;font-weight:900;color:white;">
        TATA IPL
    </div>
    <div style="font-size:25px;font-weight:900;color:#FFD21F;">
        AUCTION ANALYSIS
    </div>
    <div style="font-size:12px;color:#BDEBFF;">
        Explore. Analyze. Discover.
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🏆 Select Team")

teams = sorted(auction_df["Team"].dropna().unique())

selected_teams = st.sidebar.multiselect(
    "Teams",
    teams,
    default=teams
)

st.sidebar.markdown("### 🎯 Select Role")

roles = sorted(auction_df["Role"].dropna().unique())

selected_roles = st.sidebar.multiselect(
    "Roles",
    roles,
    default=roles
)

st.sidebar.markdown("### 🌍 Select Country")

countries = sorted(auction_df["Country"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "Countries",
    countries,
    default=countries
)

st.sidebar.markdown("""
<hr>
<div style="text-align:center;padding:15px;">
    <div style="font-size:75px;">🏆</div>
    <div style="font-size:20px;color:#FFD21F;font-weight:900;">
        IPL CHAMPIONS
    </div>
    <div style="color:#BDEBFF;font-size:11px;">
        INDIAN PREMIER LEAGUE
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# FILTER DATA
# =====================================================
df = auction_df[
    auction_df["Team"].isin(selected_teams)
    & auction_df["Role"].isin(selected_roles)
    & auction_df["Country"].isin(selected_countries)
].copy()

if df.empty:
    st.warning("No data available. Please change filters.")
    st.stop()


# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div style="
background:linear-gradient(100deg,#071A43,#102B60,#071A43);
border-radius:14px;
padding:20px;
border:1px solid #174EAA;
margin-bottom:18px;
">
<div style="font-size:36px;font-weight:900;font-style:italic;">
👑 IPL Auction Dashboard
</div>
<div style="color:#65DFFF;font-size:14px;">
Player Performance & Value for Money Analysis | 2025-2026
</div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# KPI CARDS
# =====================================================
total_players = len(df)
total_spending = df["Sold Price"].sum()

highest_bid = df["Sold Price"].max()
highest_player = df.loc[
    df["Sold Price"].idxmax(), "Player"
]

teams_count = df["Team"].nunique()

kpis = [
    ("👥", total_players, "Total Players",
     "Unique auction players",
     "linear-gradient(120deg,#BD00E8,#7100AD)"),

    ("🪙", f"₹{total_spending:.2f} Cr",
     "Selected Sample Spend",
     "19-player 2025 auction sample",
     "linear-gradient(120deg,#009BEA,#0649C9)"),

    ("⭐", f"₹{highest_bid:.2f} Cr",
     "Highest Bid",
     highest_player,
     "linear-gradient(120deg,#00B879,#007C62)"),

    ("🏆", teams_count,
     "Teams Involved",
     "Selected teams",
     "linear-gradient(120deg,#FF9B00,#F04400)")
]

cols = st.columns(4)

for col, item in zip(cols, kpis):

    icon, value, label, note, color = item

    with col:
        st.markdown(f"""
        <div class="kpi-card" style="background:{color};">
            <div style="font-size:30px;">{icon}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# CHART STYLE
# =====================================================
def style_chart(fig, height=320):

    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=11),
        margin=dict(l=35, r=20, t=35, b=35)
    )

    fig.update_xaxes(
        gridcolor="rgba(120,160,220,.12)"
    )

    fig.update_yaxes(
        gridcolor="rgba(120,160,220,.12)"
    )

    return fig


# =====================================================
# TEAM SPENDING AND TOP PLAYERS
# =====================================================
st.markdown(
    '<div class="section-title">📊 Selected-Player Spend by Team</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.5, 1])

with left:

    team_spending = (
        df.groupby("Team", as_index=False)["Sold Price"]
        .sum()
        .sort_values("Sold Price", ascending=False)
    )

    fig = px.bar(
        team_spending,
        x="Team",
        y="Sold Price",
        color="Team",
        text="Sold Price",
        color_discrete_map=TEAM_COLORS
    )

    fig.update_traces(
        texttemplate="%{y:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Team",
        yaxis_title="Auction Spending (₹ Cr)"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

with right:

    st.markdown(
        '<div class="section-title">👑 Top 5 Sold Players</div>',
        unsafe_allow_html=True
    )

    top5 = df.nlargest(5, "Sold Price")

    st.dataframe(
        top5[["Player", "Team", "Sold Price"]],
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# VALUE FOR MONEY CALCULATIONS
# =====================================================
df["Runs_Per_Crore"] = (
    df["Runs"] / df["Sold Price"]
)

df["Wickets_Per_Crore"] = (
    df["Wickets"] / df["Sold Price"]
)

batters = df[
    df["Role"].isin(["Batsman", "Wicketkeeper"])
].copy()

bowlers = df[
    df["Role"] == "Bowler"
].copy()

all_rounders = df[
    df["Role"] == "All-Rounder"
].copy()


# =====================================================
# BATTER RANKING
# =====================================================
st.markdown("---")
st.markdown(
    '<div class="section-title">🏏 Batter Value-for-Money Ranking</div>',
    unsafe_allow_html=True
)

st.caption(
    "Metric: Runs per crore = Total Runs / 2025 Sold Price. "
    "Higher value indicates more runs for the auction amount."
)

if not batters.empty:

    batters = batters.sort_values(
        "Runs_Per_Crore", ascending=False
    )

    fig = px.bar(
        batters,
        x="Player",
        y="Runs_Per_Crore",
        color="Runs_Per_Crore",
        color_continuous_scale="Turbo",
        text="Runs_Per_Crore",
        hover_data=["Runs", "Sold Price"]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    st.plotly_chart(
        style_chart(fig, 380),
        use_container_width=True
    )

    st.dataframe(
        batters[
            ["Player", "Team", "Runs",
             "Sold Price", "Runs_Per_Crore"]
        ].rename(columns={
            "Runs_Per_Crore": "Runs per Crore"
        }),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# BOWLER RANKING
# =====================================================
st.markdown("---")
st.markdown(
    '<div class="section-title">🎯 Bowler Value-for-Money Ranking</div>',
    unsafe_allow_html=True
)

st.caption(
    "Metric: Wickets per crore = Total Wickets / 2025 Sold Price. "
    "Economy is shown as a supporting metric; lower economy is better."
)

if not bowlers.empty:

    bowlers = bowlers.sort_values(
        "Wickets_Per_Crore", ascending=False
    )

    fig = px.bar(
        bowlers,
        x="Player",
        y="Wickets_Per_Crore",
        color="Wickets_Per_Crore",
        color_continuous_scale="Plasma",
        text="Wickets_Per_Crore",
        hover_data=["Wickets", "Economy", "Sold Price"]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    st.plotly_chart(
        style_chart(fig, 380),
        use_container_width=True
    )

    st.dataframe(
        bowlers[
            ["Player", "Team", "Wickets",
             "Sold Price", "Wickets_Per_Crore", "Economy"]
        ].rename(columns={
            "Wickets_Per_Crore": "Wickets per Crore"
        }),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# ALL-ROUNDER ANALYSIS
# =====================================================
st.markdown("---")
st.markdown(
    '<div class="section-title">💪 All-Rounder Analysis</div>',
    unsafe_allow_html=True
)

st.caption(
    "Runs per crore and wickets per crore are shown separately. "
    "No combined score or arbitrary weighting is used."
)

if not all_rounders.empty:

    all_rounders = all_rounders.sort_values(
        "Runs_Per_Crore", ascending=False
    )

    st.dataframe(
        all_rounders[
            ["Player", "Team", "Runs", "Wickets",
             "Sold Price", "Runs_Per_Crore",
             "Wickets_Per_Crore"]
        ].rename(columns={
            "Runs_Per_Crore": "Runs per Crore",
            "Wickets_Per_Crore": "Wickets per Crore"
        }),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# TWO-SEASON RELATIVE VALUE / OVERPAYMENT SIGNAL
# =====================================================
st.markdown("---")
st.markdown(
    '<div class="section-title">💰 Two-Season Relative Overpaid / Underpaid Analysis</div>',
    unsafe_allow_html=True
)

st.info(
    "The 2025 tab uses 2025 performance divided by the 2025 sold price. "
    "The 2026 tab uses 2026 performance divided by that SAME 2025 auction price "
    "as a benchmark; it is not a 2026 auction-price comparison. Lowest value is "
    "a screening signal, not proof of objective overpayment."
)

value_df = original_df[
    original_df["Team"].isin(selected_teams)
    & original_df["Role"].isin(selected_roles)
    & original_df["Country"].isin(selected_countries)
].copy()
value_df["Runs_Per_Crore"] = value_df["Runs"] / value_df["Sold Price"]
value_df["Wickets_Per_Crore"] = value_df["Wickets"] / value_df["Sold Price"]

season_tabs = st.tabs(["2025 auction season", "2026 performance benchmark"])

for season_tab, season_value in zip(season_tabs, [2025, 2026]):
    with season_tab:
        season_df = value_df[value_df["Season"] == season_value].copy()
        if season_value == 2026:
            st.caption("Reference denominator: each player's 2025 auction sold price (₹ crore).")
        batter_values = season_df[
            season_df["Role"].isin(["Batsman", "Wicketkeeper"])
        ].sort_values("Runs_Per_Crore", ascending=False)
        bowler_values = season_df[
            season_df["Role"] == "Bowler"
        ].sort_values("Wickets_Per_Crore", ascending=False)
        category_tabs = st.tabs(["Batters / Wicketkeepers", "Bowlers"])
        with category_tabs[0]:
            if not batter_values.empty:
                low, high = batter_values.iloc[-1], batter_values.iloc[0]
                c1, c2 = st.columns(2)
                c1.metric("Lowest relative batter value", low["Player"], f"{low['Runs_Per_Crore']:.2f} runs/crore")
                c2.metric("Highest relative batter value", high["Player"], f"{high['Runs_Per_Crore']:.2f} runs/crore")
                st.dataframe(
                    batter_values[["Player", "Team", "Runs", "Sold Price", "Runs_Per_Crore"]].rename(
                        columns={"Runs_Per_Crore": "Runs per crore"}
                    ), use_container_width=True, hide_index=True
                )
        with category_tabs[1]:
            if not bowler_values.empty:
                low, high = bowler_values.iloc[-1], bowler_values.iloc[0]
                c1, c2 = st.columns(2)
                c1.metric("Lowest relative bowler value", low["Player"], f"{low['Wickets_Per_Crore']:.2f} wickets/crore")
                c2.metric("Highest relative bowler value", high["Player"], f"{high['Wickets_Per_Crore']:.2f} wickets/crore")
                st.dataframe(
                    bowler_values[["Player", "Team", "Wickets", "Sold Price", "Wickets_Per_Crore", "Economy"]].rename(
                        columns={"Wickets_Per_Crore": "Wickets per crore"}
                    ), use_container_width=True, hide_index=True
                )


# =====================================================
# SEASON COMPARISON
# =====================================================
st.markdown("---")
st.markdown(
    '<div class="section-title">📈 2025 vs 2026 Performance Comparison</div>',
    unsafe_allow_html=True
)

comparison = comparison_df.copy()

if {"Runs_2025", "Runs_2026"}.issubset(comparison.columns):

    run_data = comparison.melt(
        id_vars="Player",
        value_vars=["Runs_2025", "Runs_2026"],
        var_name="Season",
        value_name="Runs"
    )

    run_data["Season"] = run_data["Season"].replace({
        "Runs_2025": "2025",
        "Runs_2026": "2026"
    })

    fig = px.bar(
        run_data,
        x="Player",
        y="Runs",
        color="Season",
        barmode="group",
        color_discrete_map={
            "2025": "#168BFF",
            "2026": "#FF8A16"
        }
    )

    st.plotly_chart(
        style_chart(fig, 420),
        use_container_width=True
    )

if {"Wickets_2025", "Wickets_2026"}.issubset(comparison.columns):

    wicket_data = comparison.melt(
        id_vars="Player",
        value_vars=["Wickets_2025", "Wickets_2026"],
        var_name="Season",
        value_name="Wickets"
    )

    wicket_data["Season"] = wicket_data["Season"].replace({
        "Wickets_2025": "2025",
        "Wickets_2026": "2026"
    })

    fig = px.bar(
        wicket_data,
        x="Player",
        y="Wickets",
        color="Season",
        barmode="group",
        color_discrete_map={
            "2025": "#00C98B",
            "2026": "#E83DA9"
        }
    )

    st.plotly_chart(
        style_chart(fig, 420),
        use_container_width=True
    )

st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)


# =====================================================
# NEXT AUCTION TARGETS
# =====================================================
st.markdown("---")
st.markdown(
    '<div class="section-title">🎯 Next Auction Target Shortlist</div>',
    unsafe_allow_html=True
)

st.caption(
    "Illustrative shortlist from this dataset using 2026 performance. "
    "These are performance-based candidates, not confirmed auction availability."
)

season_2026 = original_df[
    original_df["Season"] == 2026
].copy()

if not season_2026.empty:

    target_batters = season_2026[
        season_2026["Role"].isin(["Batsman", "Wicketkeeper"])
    ].sort_values("Runs", ascending=False)

    target_bowlers = season_2026[
        season_2026["Role"] == "Bowler"
    ].sort_values("Wickets", ascending=False)

    target_allrounders = season_2026[
        season_2026["Role"] == "All-Rounder"
    ].sort_values(["Runs", "Wickets"], ascending=[False, False])

    targets = []

    if not target_batters.empty:
        targets.append((
            "Top Batter",
            target_batters.iloc[0],
            "Highest runs among batters/wicketkeepers"
        ))

    if not target_bowlers.empty:
        targets.append((
            "Top Bowler",
            target_bowlers.iloc[0],
            "Highest wickets among bowlers"
        ))

    if not target_allrounders.empty:
        targets.append((
            "Top All-Rounder",
            target_allrounders.iloc[0],
            "Highest runs among all-rounders"
        ))

    target_cols = st.columns(max(1, len(targets)))

    for col, target in zip(target_cols, targets):

        label, player, reason = target

        with col:
            st.markdown(f"""
            <div class="kpi-card"
            style="background:linear-gradient(120deg,#102E67,#47208A);
            border:1px solid #4B9DFF;">
                <div style="font-size:25px;">🎯 {label}</div>
                <div class="kpi-value">{player['Player']}</div>
                <div class="kpi-note">
                    Runs: {int(player['Runs'])}<br>
                    Wickets: {int(player['Wickets'])}<br>
                    {reason}
                </div>
            </div>
            """, unsafe_allow_html=True)


# =====================================================
# COMPLETE PLAYER DATA
# =====================================================
st.markdown("---")

with st.expander("📋 View Complete 2025 Auction Data"):

    st.dataframe(
        df.sort_values("Sold Price", ascending=False),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# DATA LIMITATIONS
# =====================================================
st.markdown("---")

with st.expander("ℹ️ Data Notes & Limitations"):

    st.markdown("""
    - Auction prices in this analysis are from the 2025 auction dataset.
    - 2026 charts compare player performance, not 2026 auction prices.
    - Runs per crore and wickets per crore are role-specific metrics.
    - Bowling economy is a supporting metric; lower economy is better.
    - Player performance depends on playing time, team, role and match conditions.
    - The shortlist is based only on players included in this dataset.
    - Relative value rankings do not prove that a player was objectively overpaid or underpaid.
    """)


# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<hr>
<div style="text-align:center;padding:18px;color:#8FB8E8;
font-size:11px;letter-spacing:2px;">
🏏 IPL AUCTION ANALYTICS DASHBOARD<br><br>
PYTHON · PANDAS · STREAMLIT · PLOTLY
</div>
""", unsafe_allow_html=True)
