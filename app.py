import streamlit as st
import pandas as pd
import numpy as np
import requests
import os

st.write("CWD:", os.getcwd())
st.write("Files:", os.listdir())
st.write("ML folder:", os.listdir("ml"))
st.write("Ingestion folder:", os.listdir("ingestion"))
st.write("Utils folder:", os.listdir("utils"))

st.write("CWD:", os.getcwd())
st.write("Files:", os.listdir())

from ingestion.odds_api import fetch_ncaab_odds
from ingestion.stats_api import fetch_team_stats
from ml_engine.feature_engineering import merge_odds_and_stats
from ml_engine.predict import predict_edges


# ----------------------------------------------------
# LOAD LIVE ODDS + TEAM STATS + ML EDGE
# ----------------------------------------------------
odds_df = fetch_ncaab_odds()
stats_df = fetch_team_stats()

merged_df = merge_odds_and_stats(odds_df, stats_df)
final_df = predict_edges(merged_df)

# ----------------------------------------------------
# SAFE NUMERIC WRAPPER
# ----------------------------------------------------
def num(x):
    try:
        return float(x)
    except:
        return 0.0

# ----------------------------------------------------
# STREAMLIT PAGE CONFIG + STYLES
# ----------------------------------------------------
st.set_page_config(
    page_title="Full Court Analytics",
    page_icon="https://raw.githubusercontent.com/davidchestang02-dev/full-court-analytics/main/images/fca_logo.png",
    layout="wide"
)

st.markdown("""
<style>
/* (your full CSS exactly as you had it) */
...
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top: 0.4rem; margin-bottom: -0.4rem;">
        <img src="https://raw.githubusercontent.com/davidchestang02-dev/full-court-analytics/main/images/fca_logo.png"
             style="width:760px; filter: drop-shadow(0 0 26px rgba(80,120,255,0.75));">
    </div>

    <div style="
        text-align: center;
        font-size: 1.95rem;
        font-weight: 900;
        margin-top: -0.15rem;
        margin-bottom: 2.5rem;
        letter-spacing: 0.34em;
        text-transform: uppercase; 
        color: #ffffff;
        -webkit-text-stroke: 1px rgba(0,25,90,0.65);
        text-shadow:
            0 0 10px rgba(0,25,90,1.0),
            0 0 22px rgba(60,110,220,0.95),
            0 0 42px rgba(140,170,255,0.85),
            0 0 70px rgba(160,190,255,0.75);
    ">
        Model‑Driven Betting Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------
# SAFE HTML TABLE LOADER (TEAMRANKINGS HTML)
# ----------------------------------------------------
@st.cache_data(ttl=21600)
def load_stat(url, label):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        from io import StringIO
        tables = pd.read_html(StringIO(response.text))

        if not tables:
            st.write(f"{label} → No tables found.")
            return None

        df = tables[0].copy()

        if "Team" not in df.columns:
            st.write(f"{label} → Unexpected columns: {df.columns.tolist()}")
            return None

        stat_col = df.columns[-1]
        df = df.loc[:, ["Team", stat_col]].copy()
        df.columns = ["Team", label]
        df.loc[:, "Team"] = df["Team"].str.strip()

        return df

    except Exception as e:
        st.write(f"{label} → ERROR: {e}")
        return None

# ----------------------------------------------------
# STABLE STAT LIST (TEAMRANKINGS)
# ----------------------------------------------------
STAT_SPECS = [
    ("https://www.teamrankings.com/ncaa-basketball/stat/offensive-efficiency", "OffEff"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/defensive-efficiency", "DefEff"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/possessions-per-game", "Pace"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/two-point-rate", "TwoPRate"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/two-point-pct", "TwoPPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/three-point-rate", "ThreePRate"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/three-point-pct", "ThreePPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/fta-per-fga", "FTAperFGA"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/free-throw-rate", "FTRate"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/free-throw-pct", "FTPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/turnover-pct", "TOVPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/offensive-rebounding-pct", "OffRebPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/defensive-rebounding-pct", "DefRebPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/average-scoring-margin", "AvgScoreMargin"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-two-point-rate", "OppTwoPRate"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-two-point-pct", "OppTwoPPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-three-point-rate", "OppThreePRate"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-three-point-pct", "OppThreePPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-free-throw-pct", "OppFTPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-free-throw-rate", "OppFTRate"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-fta-per-fga", "OppFTAperFGA"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-effective-field-goal-pct", "OppeFG"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-offensive-rebounding-pct", "OppOffRebPct"),
    ("https://www.teamrankings.com/ncaa-basketball/stat/opponent-defensive-rebounding-pct", "OppDefRebPct"),
]

# ----------------------------------------------------
# BUILD TEAMSTATS
# ----------------------------------------------------
team_stats = None
for url, label in STAT_SPECS:
    df = load_stat(url, label)
    if df is None:
        continue
    if team_stats is None:
        team_stats = df
    else:
        team_stats = team_stats.merge(df, on="Team", how="inner")

if team_stats is None or team_stats.empty:
    st.error("No valid TeamRankings tables were loaded.")
    st.stop()

team_stats_dict = team_stats.set_index("Team").to_dict(orient="index")

# ----------------------------------------------------
# GAME SELECTION FROM LIVE ODDS + ML
# ----------------------------------------------------
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
st.markdown('<div class="tournament-header">MATCHUP SELECTION</div>', unsafe_allow_html=True)

games = final_df[["home_team", "away_team"]].drop_duplicates()
game_labels = [
    f"{row.home_team} vs {row.away_team}"
    for row in games.itertuples()
]

selected_game = st.selectbox("Select Game (Live Odds + ML)", game_labels)

home_team, away_team = selected_game.split(" vs ")

game_row = final_df[
    (final_df["home_team"] == home_team) &
    (final_df["away_team"] == away_team)
].iloc[0]

api_spread_home = float(game_row["spread_home"]) if game_row["spread_home"] is not None else 0.0
api_total = float(game_row["total_points"]) if game_row["total_points"] is not None else 145.5
ml_edge = float(game_row["ml_edge"])

# ----------------------------------------------------
# MATCHUP + MARKET (UI)
# ----------------------------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("<div class='section-header'>Matchup</div>", unsafe_allow_html=True)
    team_a = st.selectbox("Home Team", list(team_stats_dict.keys()), index=list(team_stats_dict.keys()).index(home_team) if home_team in team_stats_dict else 0, key="team_a")
    team_b = st.selectbox("Away Team", list(team_stats_dict.keys()), index=list(team_stats_dict.keys()).index(away_team) if away_team in team_stats_dict else 1, key="team_b")

with col_right:
    st.markdown("<div class='section-header'>Market Odds</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Point Spread (Home)</div>
        </div>
    """, unsafe_allow_html=True)
    market_spread = st.number_input(" ", value=api_spread_home, step=0.5, key="market_spread")

    st.markdown("""
        <div class="metric-card" style="margin-top: 1rem;">
            <div class="metric-label">Game Total</div>
        </div>
    """, unsafe_allow_html=True)
    market_total = st.number_input("  ", value=api_total, step=0.5, key="market_total")

    st.markdown("""
        <div class="metric-card" style="margin-top: 1rem;">
            <div class="metric-label">ML Edge</div>
            <div class="metric-value">{:.2f}</div>
            <div class="metric-sub">Probability market is wrong</div>
        </div>
    """.format(ml_edge), unsafe_allow_html=True)

a = team_stats_dict[team_a]
b = team_stats_dict[team_b]

# ----------------------------------------------------
# DETERMINISTIC ENGINE (RAW BASELINE)
# ----------------------------------------------------
off_a = num(a.get("OffEff"))
off_b = num(b.get("OffEff"))
def_a = num(a.get("DefEff"))
def_b = num(b.get("DefEff"))
pace_a = num(a.get("Pace"))
pace_b = num(b.get("Pace"))

avg_poss = (pace_a + pace_b) / 2

two_p_rate_home = num(a.get("TwoPRate"))
three_p_rate_home = num(a.get("ThreePRate"))
ft_rate_home = num(a.get("FTRate"))

two_p_rate_away = num(b.get("TwoPRate"))
three_p_rate_away = num(b.get("ThreePRate"))
ft_rate_away = num(b.get("FTRate"))

two_p_pct_home = num(a.get("TwoPPct"))
two_p_pct_away = num(b.get("TwoPPct"))
opp_two_p_pct_home = num(a.get("OppTwoPPct"))
opp_two_p_pct_away = num(b.get("OppTwoPPct"))

three_p_pct_home = num(a.get("ThreePPct"))
three_p_pct_away = num(b.get("ThreePPct"))
opp_three_p_pct_home = num(a.get("OppThreePPct"))
opp_three_p_pct_away = num(b.get("OppThreePPct"))

ft_pct_home = num(a.get("FTPct"))
ft_pct_away = num(b.get("FTPct"))
opp_ft_pct_home = num(a.get("OppFTPct"))
opp_ft_pct_away = num(b.get("OppFTPct"))

adj_2p_home = two_p_pct_home * (1 - (opp_two_p_pct_away - two_p_pct_home))
adj_3p_home = three_p_pct_home * (1 - (opp_three_p_pct_away - three_p_pct_home))
adj_ft_rate_home = ft_rate_home * (1 - (opp_ft_pct_away - ft_rate_home))

adj_2p_away = two_p_pct_away * (1 - (opp_two_p_pct_home - two_p_pct_away))
adj_3p_away = three_p_pct_away * (1 - (opp_three_p_pct_home - three_p_pct_away))
adj_ft_rate_away = ft_rate_away * (1 - (opp_ft_pct_home - ft_rate_away))

tov_home = num(a.get("TOVPct"))
tov_away = num(b.get("TOVPct"))

adj_poss_home = avg_poss * (1 - tov_home)
adj_poss_away = avg_poss * (1 - tov_away)
avg_adj_poss = (adj_poss_home + adj_poss_away) / 2

off_reb_home = num(a.get("OffRebPct"))
off_reb_away = num(b.get("OffRebPct"))

extra_poss_home = avg_poss * off_reb_home
extra_poss_away = avg_poss * off_reb_away
avg_extra_poss = (extra_poss_home + extra_poss_away) / 2

adjusted_poss_rate = avg_poss + avg_extra_poss
final_poss_rate = (adjusted_poss_rate + avg_poss) / 2

eff_scoring_home = off_a * (def_b / 1.05)
eff_scoring_away = off_b * (def_a / 1.05)

proj_a = eff_scoring_home * final_poss_rate
proj_b = eff_scoring_away * final_poss_rate
proj_total = proj_a + proj_b
proj_spread = proj_a - proj_b  # home - away

# ----------------------------------------------------
# EDGES VS MARKET
# ----------------------------------------------------
true_market_spread = -market_spread
spread_edge = proj_spread - true_market_spread
total_edge = proj_total - market_total

spread_edge_display = abs(spread_edge)
total_edge_display = abs(total_edge)

# ----------------------------------------------------
# IDENTIFY FAVORITE & UNDERDOG FROM MARKET SPREAD
# ----------------------------------------------------
if market_spread < 0:
    favorite = team_a
    underdog = team_b
elif market_spread > 0:
    favorite = team_b
    underdog = team_a
else:
    favorite = None
    underdog = None

spread_edge_team = favorite if spread_edge > 0 else underdog
total_edge_side = "Over" if total_edge > 0 else "Under"

# ----------------------------------------------------
# SIM DEFAULTS
# ----------------------------------------------------
sigma = 12.0
num_sims = 10000

with st.expander("Simulation Controls", expanded=False):
    s1, s2 = st.columns(2)
    with s1:
        volatility = st.slider("Volatility", 5.0, 25.0, 12.0, step=1.0)
    with s2:
        num_sims = st.slider("Simulations", 2000, 30000, 14000, step=1000)
    sigma = float(volatility)
    num_sims = int(num_sims)

# ----------------------------------------------------
# MONTE CARLO ENGINE
# ----------------------------------------------------
np.random.seed(42)
sim_a = np.random.normal(proj_a, sigma, num_sims)
sim_b = np.random.normal(proj_b, sigma, num_sims)

sim_spread = sim_a - sim_b
sim_total = sim_a + sim_b

prob_a_covers = float(np.mean(sim_spread > true_market_spread))
prob_b_covers = float(np.mean(sim_spread < true_market_spread))
prob_push_spread = float(np.mean(np.isclose(sim_spread, true_market_spread, atol=0.5)))

prob_over = float(np.mean(sim_total > market_total))
prob_under = float(np.mean(sim_total < market_total))
prob_push_total = float(np.mean(np.isclose(sim_total, market_total, atol=0.5)))

# ----------------------------------------------------
# DASHBOARD LAYOUT
# ----------------------------------------------------
col_main, col_side = st.columns([2.2, 1.3])

with col_main:
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="tournament-header">SCOREBOARD PROJECTIONS</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1], gap="large")

    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{team_a}</div>
                <div class="metric-value">{proj_a:.1f}</div>
                <div class="metric-sub">Projected Score</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{team_b}</div>
                <div class="metric-value">{proj_b:.1f}</div>
                <div class="metric-sub">Projected Score</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total</div>
                <div class="metric-value">{proj_total:.1f}</div>
                <div class="metric-sub">Projected Total</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="tournament-header">SIMULATION SUMMARY</div>', unsafe_allow_html=True)

    ss1, ss2, ss3 = st.columns([1, 1, 1], gap="large")

    with ss1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Cover Probability</div>
                <div class="metric-value">{prob_a_covers:.1%}</div>
                <div class="metric-sub">{team_a} covers {market_spread:+.1f}</div>
            </div>
        """, unsafe_allow_html=True)

    with ss2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Cover Probability</div>
                <div class="metric-value">{prob_b_covers:.1%}</div>
                <div class="metric-sub">{team_b} covers {abs(market_spread):+.1f}</div>
            </div>
        """, unsafe_allow_html=True)

    with ss3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Push Probability</div>
                <div class="metric-value">{prob_push_spread:.1%}</div>
                <div class="metric-sub">Spread push</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    spread_pick_side = team_a if spread_edge > 0 else team_b
    total_pick_side = "Over" if total_edge > 0 else "Under"

    def edge_color(edge, strong_threshold, weak_threshold=0):
        abs_edge = abs(edge)
        if abs_edge >= strong_threshold:
            return "edge-green"
        if abs_edge >= weak_threshold:
            return "edge-yellow"
        return "edge-red"

    spread_edge_class = edge_color(spread_edge, strong_threshold=1.25)
    total_edge_class = edge_color(total_edge, strong_threshold=5.0, weak_threshold=2.5)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="tournament-header">MODEL VS MARKET</div>', unsafe_allow_html=True)

    mv1, mv2 = st.columns(2, gap="large")

    with mv1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Spread Edge</div>
                <div class="metric-value {spread_edge_class}">{spread_edge:+.1f}</div>
                <div class="metric-sub">{spread_edge_team} vs Market {market_spread:+.1f}</div>
            </div>
        """, unsafe_allow_html=True)

    with mv2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Edge</div>
                <div class="metric-value {total_edge_class}">{total_edge:+.1f}</div>
                <div class="metric-sub">{total_edge_side} vs {market_total:.1f}</div>
            </div>
        """, unsafe_allow_html=True)

with col_side:
    # RELIABILITY SCORE (NO WEIGHTS, PURE SIM CONFIDENCE)
    spread_conf = max(prob_a_covers, prob_b_covers)
    total_conf = max(prob_over, prob_under)

    reliability = (spread_conf + total_conf) / 2
    rel_score = reliability * 100
    percent = max(0, min(rel_score, 100))

    if percent < 25:
        rel_color = "#b30000"
    elif percent < 51:
        rel_color = "#ff4d4d"
    elif percent < 66:
        rel_color = "#7dffb0"
    else:
        rel_color = "#4dff88"

    st.markdown(
        f"""
        <div class="reliability-circle"
             style="
                background:
                    radial-gradient(circle, rgba(25,35,55,0.75) 60%, transparent 61%),
                    conic-gradient({rel_color} {percent}%, rgba(60,60,80,0.25) {percent}%);
                box-shadow:
                    0 0 22px {rel_color},
                    0 0 44px {rel_color}88;
             ">
            <div class="reliability-inner" 
                 style="
                    color:{rel_color};
                    text-shadow:
                        0 0 12px {rel_color},
                        0 0 24px {rel_color}aa,
                        0 0 36px {rel_color}88;
                 ">
                {percent:.1f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------------------------
# RIGHT COLUMN (optional)
# ----------------------------------------------------
with col_side:
    # You can put matchup info, market info, team logos, etc.
    pass


























































































































