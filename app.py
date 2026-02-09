import streamlit as st
import pandas as pd
import numpy as np
import requests

# ----------------------------------------------------
# SAFE NUMERIC WRAPPER
# ----------------------------------------------------
def num(x):
    try:
        return float(x)
    except:
        return 0.0

# ----------------------------------------------------
st.set_page_config(
    page_title="CBB Algorithmic Projection Engine",
    page_icon="🏀",
    layout="wide",
)

st.markdown(
    """
    <style>

    /* GLOBAL ------------------------------------------------------------ */
    .stApp {
        background-image: url("https://i.imgur.com/rdqEqhv.jpeg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #e8ecff;
        font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }


    .css-1y4p8pa, .css-1v0mbdj, .css-1dp5vir {
        margin-top: -0.5rem !important;
        padding-top: 0rem !important;
    }

    .block-container {
        padding-top: 0.5rem !important;
    }
    
    /* Fully fix team name cutoff in selectboxes */
    .stSelectbox > div {
        width: 100% !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        width: 100% !important;
        max-width: 100% !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        width: 100% !important;
        max-width: 100% !important;
    }

    .stSelectbox div[data-baseweb="select"] span {
        width: 100% !important;
        max-width: 100% !important;
        white-space: nowrap !important;
        overflow: visible !important;
    }

    /* HEADERS ----------------------------------------------------------- */
    h1, h2, h3, h4 {
        color: #e8ecff;
        text-shadow: 0 0 18px rgba(80,120,255,0.75) !important;
        letter-spacing: 0.04em;
    }

    /* INPUTS ------------------------------------------------------------ */
    .stSelectbox > div > div {
        background: rgba(20,25,45,0.85) !important;
        border: 1px solid rgba(90,120,255,0.35) !important;
        border-radius: 0.6rem !important;
        color: #e8ecff !important;
    }

    .stSelectbox > div > div {
        min-height: 2.2rem !important;
        padding-top: 0.15rem !important;
        padding-bottom: 0.15rem !important;
    }

    .stNumberInput > div > div > input {
        background: rgba(20,25,45,0.85) !important;
        border: 1px solid rgba(90,120,255,0.35) !important;
        border-radius: 0.6rem !important;
        color: #e8ecff !important;
    }

    .stSlider > div > div > div {
        background: rgba(80,120,255,0.45) !important;
    }

    /* BUTTONS ----------------------------------------------------------- */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
        color: white;
        border-radius: 0.6rem;
        padding: 0.6rem 1.2rem;
        border: none;
        font-weight: 600;
        letter-spacing: 0.05em;
        transition: 0.25s ease;
        box-shadow: 0 0 12px rgba(0, 200, 255, 0.35);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 18px rgba(0, 200, 255, 0.55);
    }

    /* METRIC CARDS ------------------------------------------------------ */
    .metric-card {
        padding: 1rem 1.25rem;
        border-radius: 0.9rem;
        background: rgba(15,20,35,0.85);
        border: 1px solid rgba(80,120,255,0.35);
        box-shadow: 0 0 18px rgba(0, 120, 255, 0.15);
        transition: 0.25s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 28px rgba(0, 150, 255, 0.35);
    }

    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #a5b4fc;
        letter-spacing: 0.12em;
    }

    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #7dd3fc;
        text-shadow: 0 0 10px rgba(0,200,255,0.45);
    }

    .metric-sub {
        font-size: 0.8rem;
        color: #9ca3af;
    }

    /* TABLE -------------------------------------------------------------- */
    .dataframe {
        background: rgba(10,15,30,0.75);
        border-radius: 0.6rem;
        border: 1px solid rgba(80,120,255,0.25);
        color: #e8ecff;
    }

    .dataframe th {
        background: rgba(20,30,60,0.85);
        color: #a5b4fc;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .dataframe td {
        background: rgba(10,15,30,0.55);
    }

    /* SECTION HEADERS ---------------------------------------------------- */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
        color: #a5b4fc;
        text-shadow: 0 0 12px rgba(80,120,255,0.35);
    }

    </style>
    """,
unsafe_allow_html=True,
)
# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown("""
<div style="
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 0.5rem;
    margin-bottom: 1.25rem;
">
    <h1 style="
        font-size: 3.6rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        background: linear-gradient(90deg, #60a5fa, #7dd3fc, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 22px rgba(80,120,255,0.45);
        text-align: center;
    ">
        Full Court Analytics
    </h1>
</div>
""", unsafe_allow_html=True)
# ----------------------------------------------------
# SAFE HTML TABLE LOADER (YEAR-BASED)
# ----------------------------------------------------
@st.cache_data(ttl=21600)
def load_stat(url, label):
    csv_url = url + "/download?format=csv"

    try:
        df = pd.read_csv(csv_url)
        if "Team" not in df.columns:
            return None

        df = df[["Team", df.columns[-1]]]
        df.columns = ["Team", label]
        df["Team"] = df["Team"].str.strip()
        return df

    except Exception:
        return None
# ----------------------------------------------------
# STABLE STAT LIST (24 WORKING URLS)
# ----------------------------------------------------
STAT_SPECS = [
("https://www.teamrankings.com/ncaa-basketball/stat/offensive-efficiency/download?format=csv", "OffEff"),
("https://www.teamrankings.com/ncaa-basketball/stat/defensive-efficiency/download?format=csv", "DefEff"),
("https://www.teamrankings.com/ncaa-basketball/stat/possessions-per-game/download?format=csv", "Pace"),
("https://www.teamrankings.com/ncaa-basketball/stat/two-point-rate/download?format=csv", "TwoPRate"),
("https://www.teamrankings.com/ncaa-basketball/stat/two-point-pct/download?format=csv", "TwoPPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/three-point-rate/download?format=csv", "ThreePRate"),
("https://www.teamrankings.com/ncaa-basketball/stat/three-point-pct/download?format=csv", "ThreePPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/fta-per-fga/download?format=csv", "FTAperFGA"),
("https://www.teamrankings.com/ncaa-basketball/stat/free-throw-rate/download?format=csv", "FTRate"),
("https://www.teamrankings.com/ncaa-basketball/stat/free-throw-pct/download?format=csv", "FTPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/turnover-pct/download?format=csv", "TOVPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/offensive-rebounding-pct/download?format=csv", "OffRebPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/defensive-rebounding-pct/download?format=csv", "DefRebPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/average-scoring-margin/download?format=csv", "AvgScoreMargin"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-two-point-rate/download?format=csv", "OppTwoPRate"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-two-point-pct/download?format=csv", "OppTwoPPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-three-point-rate/download?format=csv", "OppThreePRate"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-three-point-pct/download?format=csv", "OppThreePPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-free-throw-pct/download?format=csv", "OppFTPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-free-throw-rate/download?format=csv", "OppFTRate"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-fta-per-fga/download?format=csv", "OppFTAperFGA"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-effective-field-goal-pct/download?format=csv", "OppeFG"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-offensive-rebounding-pct/download?format=csv", "OppOffRebPct"),
("https://www.teamrankings.com/ncaa-basketball/stat/opponent-defensive-rebounding-pct/download?format=csv", "OppDefRebPct"),

]

# ----------------------------------------------------
# BUILD TEAMSTATS
# ----------------------------------------------------
team_stats = None

st.write("Loading stats…")

for url, label in STAT_SPECS:
    st.write(f"Fetching {label}")
    
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
# TOP LAYOUT: TEAMS + MARKET + SIM SETTINGS
# ----------------------------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown(
    """
    <h3 style="
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
        color: #a5b4fc;
        text-shadow: 0 0 12px rgba(80,120,255,0.35);
    ">
        Matchup
    </h3>
    """,
    unsafe_allow_html=True,
)

    team_a = st.selectbox("Team A", list(team_stats_dict.keys()), key="team_a")
    team_b = st.selectbox("Team B", list(team_stats_dict.keys()), key="team_b")


with col_right:
    st.markdown(
    """
    <h3 style="
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
        color: #a5b4fc;
        text-shadow: 0 0 12px rgba(80,120,255,0.35);
    ">
        Market
    </h3>
    """,
    unsafe_allow_html=True,
)

    market_spread = st.number_input("Spread", value=0.0, step=0.5)
    market_total = st.number_input("Total", value=145.0, step=0.5)

    st.markdown(
    """
    <h3 style="
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
        color: #a5b4fc;
        text-shadow: 0 0 12px rgba(80,120,255,0.35);
    ">
        Simulation
    </h3>
    """,
    unsafe_allow_html=True,
)

    num_sims = st.slider("Simulations", min_value=2000, max_value=20000, value=8000, step=1000)
    sigma = st.slider("Volatility (Std Dev)", min_value=4.0, max_value=14.0, value=8.0, step=0.5)

a = team_stats_dict[team_a]
b = team_stats_dict[team_b]

# ----------------------------------------------------
# DETERMINISTIC ENGINE (OPTION B)
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
proj_spread = proj_a - proj_b

# ----------------------------------------------------
# CORRECT MARKET SPREAD INTERPRETATION
# ----------------------------------------------------
true_market_spread = -market_spread
spread_edge = proj_spread - true_market_spread
total_edge = proj_total - market_total

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
    st.markdown(
        """
        <h3 style="
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: 0.05em;
            color: #a5b4fc;
            text-shadow: 0 0 12px rgba(80,120,255,0.35);
        ">
            Projection Panel
        </h3>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">Projected Score</div>
              <div class="metric-value">{proj_a:.1f}</div>
              <div class="metric-sub">{team_a}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">Projected Score</div>
              <div class="metric-value">{proj_b:.1f}</div>
              <div class="metric-sub">{team_b}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">Projected Total</div>
              <div class="metric-value">{proj_total:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <h3 style="
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: 0.05em;
            color: #a5b4fc;
            text-shadow: 0 0 12px rgba(80,120,255,0.35);
        ">
            Model vs Market
        </h3>
        """,
        unsafe_allow_html=True,
    )

    c4, c5 = st.columns(2)

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">Spread Edge</div>
              <div class="metric-value">{spread_edge:+.1f}</div>
              <div class="metric-sub">Market: {market_spread:+.1f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c5:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">Total Edge</div>
              <div class="metric-value">{total_edge:+.1f}</div>
              <div class="metric-sub">Market: {market_total:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with col_side:
    st.markdown(
        """
        <h3 style="
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: 0.05em;
            color: #a5b4fc;
            text-shadow: 0 0 12px rgba(80,120,255,0.35);
        ">
            Simulation Summary
        </h3>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">Cover Probability</div>
          <div class="metric-value">{prob_a_covers:.1%}</div>
          <div class="metric-sub">{team_a} covers {market_spread:+.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">Cover Probability</div>
          <div class="metric-value">{prob_b_covers:.1%}</div>
          <div class="metric-sub">{team_b} covers {market_spread:+.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">Push Probability</div>
          <div class="metric-value">{prob_push_spread:.1%}</div>
          <div class="metric-sub">Spread push window</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">Total – Over</div>
          <div class="metric-value">{prob_over:.1%}</div>
          <div class="metric-sub">Over {market_total:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">Total – Under</div>
          <div class="metric-value">{prob_under:.1%}</div>
          <div class="metric-sub">Under {market_total:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">Total – Push</div>
          <div class="metric-value">{prob_push_total:.1%}</div>
          <div class="metric-sub">Total push window</div>
        </div>
        """,
        unsafe_allow_html=True,

    )

