import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import StringIO


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
    page_title="Full Court Analytics",
    page_icon="https://raw.githubusercontent.com/davidchestang02-dev/full-court-analytics/main/images/fca_logo.png",
    layout="wide"
)
st.markdown("""
<style>
/* GLOBAL ------------------------------------------------------------ */
.stApp {
    background-image: url("https://raw.githubusercontent.com/davidchestang02-dev/full-court-analytics/main/images/fca_background_1.png");
    background-size: cover;
    background-position: center 5%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    image-rendering: high-quality;
    transform: scale(.98);
    transform-origin: center center;   
    color: #e8ecff;
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(5, 10, 20, 0.35);
    z-index: -1;
}

.block-container {
    padding-top: 3.5rem !important;
}

/* HEADERS ----------------------------------------------------------- */
h1, h2, h3, h4 {
    color: #e8ecff;
    text-shadow: 0 0 18px rgba(80,120,255,0.75) !important;
    letter-spacing: 0.04em;
}

.header-logo {
    width: 480px !important;   /* bump from 420–460 to a strong 480 */
    max-width: 90% !important;
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-top: 0.5rem;
    margin-bottom: -0.5rem;
}

/* SECTION HEADERS --------------------------------------------------- */
.tournament-header {
    text-align: center;
    font-size: 1.85rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.32em !important;
    text-transform: uppercase !important;
    color: #ffffff !important;
    -webkit-text-stroke: 1px rgba(0,25,90,0.75);
    text-shadow:
        0 0 12px rgba(0,40,120,1),
        0 0 26px rgba(60,110,255,1),
        0 0 48px rgba(140,170,255,0.95),
        0 0 90px rgba(160,190,255,0.85);
    margin-top: 1.2rem !important;
    margin-bottom: 0.8rem !important;
}

/* SELECTBOXES — FINAL PREMIUM THEME ---------------------------------- */
.stSelectbox div[data-baseweb="select"] {
    background: rgba(8,12,25,0.92) !important; /* same dark fill as expanders */
    border: 3px solid rgba(80,120,255,0.65) !important; /* heavy glowing border */
    border-radius: 0.9rem !important;
    padding: 0.35rem 0.6rem !important;

    box-shadow:
        0 0 14px rgba(60,110,220,0.55),
        0 0 28px rgba(120,160,255,0.35) !important; /* same glow as expander */
}


.stSelectbox div[data-baseweb="select"] {
    background: rgba(8,12,25,0.92) !important; /* same as expanders */
    border: 3px solid rgba(80,120,255,0.65) !important;
    border-radius: 0.9rem !important;
    padding: 0.35rem 0.6rem !important;
    box-shadow:
        0 0 14px rgba(60,110,220,0.55),
        0 0 28px rgba(120,160,255,0.35) !important;
}

.stSelectbox div[data-baseweb="select"] span {
    color: #c7d2fe !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    text-shadow:
        0 0 10px rgba(80,120,255,0.75),
        0 0 22px rgba(120,160,255,0.55) !important;
}

.stSelectbox div[data-baseweb="option"] {
    background: rgba(12,18,35,0.65) !important;
    color: #e8ecff !important;
    font-weight: 600 !important;
    border-radius: 0.4rem !important;
    margin: 0.15rem 0.25rem !important;
}

.stSelectbox div[data-baseweb="option"]:hover {
    background: rgba(60,110,220,0.35) !important;
    color: #ffffff !important;

    text-shadow:
        0 0 10px rgba(80,120,255,0.75),
        0 0 22px rgba(120,160,255,0.55) !important;
}

div[data-testid="stExpander"], .stSelectbox label[data-testid="stWidgetLabel"] div[data-testid="stMarkdownContainer"] p,
label[data-testid="stWidgetLabel"] div[data-testid="stMarkdownContainer"] p {
    font-size: 1.25rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;

    background-color: rgba(12,18,35,0.55) !important;
    padding: 0.35rem 0.55rem !important;
    border-radius: 0.35rem !important;

    color: #c7d2fe !important;

    text-shadow:
        0 0 10px rgba(80,120,255,0.75),
        0 0 22px rgba(120,160,255,0.55) !important;
}


/* NUMBER INPUTS (GLOBAL) ------------------------------------------- */
input[type="number"] {
    background: rgba(20,25,45,0.9) !important;
    border: 1px solid rgba(90,120,255,0.45) !important;
    border-radius: 0.6rem !important;
    color: #e8ecff !important;
    padding: 6px 10px !important;
    font-size: 1.1rem !important;
}

/* HIDE LABEL + TIGHTEN GAP FOR NUMBER INPUTS ----------------------- */
.stNumberInput > label {
    display: none !important;
}

.stNumberInput {
    margin-top: -0.4rem !important;
}

/* METRIC CARDS ------------------------------------------------------ */
.metric-card {
    padding: 1rem 1.25rem;
    border-radius: 0.9rem;
    background: rgba(15,20,35,0.9);
    border: 1px solid rgba(80,120,255,0.45);
    box-shadow: 0 0 18px rgba(0,120,255,0.2);
    transition: 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 26px rgba(0,150,255,0.4);
}

.metric-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    color: #a5b4fc;
    letter-spacing: 0.14em;
    text-shadow: 0 0 14px rgba(80,120,255,0.55);
}

.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #7dd3fc;
    text-shadow: 0 0 10px rgba(0,200,255,0.45);
}

/* MARKET INPUTS (SPREAD / TOTAL) ----------------------------------- */
div[data-baseweb="input"] input {
    color: #7dd3fc !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(0,200,255,0.45) !important;
    text-align: center !important;
    background: rgba(10,15,30,0.9) !important;
    border: 1px solid rgba(80,120,255,0.45) !important;
    border-radius: 0.6rem !important;
    box-shadow: 0 0 12px rgba(80,120,255,0.3) !important;
}

/* +/- BUTTONS ------------------------------------------------------- */
div[data-baseweb="input"] button {
    background: rgba(20,30,60,0.9) !important;
    border: 1px solid rgba(80,120,255,0.55) !important;
    color: #a5b4fc !important;
    border-radius: 0.4rem !important;
    font-size: 1.2rem !important;
    padding: 0.2rem 0.6rem !important;
    box-shadow: 0 0 14px rgba(80,120,255,0.45) !important;
    transition: 0.2s ease;
}

div[data-baseweb="input"] button:hover {
    background: rgba(50,70,120,0.95) !important;
    border-color: rgba(140,170,255,0.85) !important;
    box-shadow: 0 0 22px rgba(120,160,255,0.75) !important;
    color: #dbe4ff !important;
}

/* OVERRIDE BASEWEB NEGATIVE/ERROR STATES --------------------------- */
div[data-baseweb="input"] button,
div[data-baseweb="input"] button:hover,
div[data-baseweb="slider"] div[role="slider"],
div[data-baseweb="slider"] div[role="slider"]:hover {
    outline: none !important;
    border-color: rgba(120,160,255,0.75) !important;
    box-shadow: 0 0 18px rgba(120,160,255,0.75) !important;
}

/* SLIDERS ----------------------------------------------------------- */
.stSlider > div[data-baseweb="slider"] > div {
    height: 12px !important;
    background: rgba(80,120,255,0.35) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 14px rgba(80,120,255,0.45) !important;
}

.stSlider > div[data-baseweb="slider"] div[role="slider"] {
    height: 22px !important;
    width: 22px !important;
    background: #7dd3fc !important;
    border: 2px solid #a5b4fc !important;
    box-shadow: 0 0 22px rgba(120,160,255,0.75) !important;
}

/* TABLE ------------------------------------------------------------- */
.dataframe {
    background: rgba(10,15,30,0.8);
    border-radius: 0.6rem;
    border: 1px solid rgba(80,120,255,0.3);
    color: #e8ecff;
}

.dataframe th {
    background: rgba(20,30,60,0.9);
    color: #a5b4fc;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.dataframe td {
    background: rgba(10,15,30,0.6);
}

/* EXPANDER CONTAINER ------------------------------------------------ */
.st-expander {
    background: rgba(6,10,20,0.92) 
    border: 3px solid rgba(80,120,255,0.75) !important;
    border-radius: 1rem !important;
    box-shadow:
        0 0 14px rgba(60,110,220,0.65),
        0 0 32px rgba(120,160,255,0.45);
    padding: 0.75rem !important;
}

details > summary,
div[data-testid="stExpander"] summary,
.st-expanderHeader,
.st-expander > details > summary {
    font-size: 1.70rem !important;
    font-weight: 920 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    background-color: rgba(12,18,35,0.55) !important;
    padding: 0.45rem !important;
    border-radius: 0.45rem !important;
    color: #c7d2fe !important;
    text-shadow:
        0 0 10px rgba(80,120,255,0.75),
        0 0 22px rgba(120,160,255,0.55);
}

.st-expander .st-expander-content {
    background: rgba(6,10,20,0.92) !important;
    border: 2px solid rgba(80,120,255,0.35) !important;
    border-radius: 0.6rem !important;
    padding: 1rem 1.2rem !important;
}


div[data-testid="stExpander"] label[data-testid="stWidgetLabel"] div[data-testid="stMarkdownContainer"] p {
    font-size: 1.25rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;

    background-color: rgba(12,18,35,0.55) !important;
    padding: 0.35rem 0.55rem !important;
    border-radius: 0.35rem !important;

    color: #c7d2fe !important;

    text-shadow:
        0 0 10px rgba(80,120,255,0.75),
        0 0 22px rgba(120,160,255,0.55);
}


/* EDGE COLORS ------------------------------------------------------- */
.edge-green {
    color: #00ff88;
    text-shadow: 0 0 10px rgba(0,255,136,0.6);
}

.edge-red {
    color: #ff4d4d;
    text-shadow: 0 0 10px rgba(255,77,77,0.6);
}

.metric-card + div[data-baseweb="input"] { margin-top: 0.9rem !important; }

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top: 0.8rem; margin-bottom: -0.2rem;">
        <img src="https://raw.githubusercontent.com/davidchestang02-dev/full-court-analytics/main/images/fca_logo.png"
             style="width:760px; filter: drop-shadow(0 0 26px rgba(80,120,255,0.75));">
    </div>

    <div style="
        text-align: center;
        font-size: 1.95rem;
        font-weight: 900;
        margin-top: -0.05rem;
        margin-bottom: 1.6rem;
        letter-spacing: 0.34em;
        text-transform: uppercase; 
        color: #ffffff;
        -webkit-text-stroke: 1px rgba(0,25,90,0.65);
        text-shadow:
            0 0 10px rgba(0,25,90,1.0),      /* deep navy inner halo (strong) */
            0 0 22px rgba(60,110,220,0.95),  /* mid blue glow (brighter) */
            0 0 42px rgba(140,170,255,0.85), /* light blue outer glow (bigger) */
            0 0 70px rgba(160,190,255,0.75); /* extended soft fade (arena effect) */
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

        # FIX: wrap HTML in StringIO to avoid FutureWarning
        from io import StringIO
        tables = pd.read_html(StringIO(response.text))

        if not tables:
            st.write(f"{label} → No tables found.")
            return None

        df = tables[0].copy()   # FIX: ensure df is a real copy, not a slice

        if "Team" not in df.columns:
            st.write(f"{label} → Unexpected columns: {df.columns.tolist()}")
            return None

        # Use the last numeric column (current season)
        stat_col = df.columns[-1]

        # FIX: safe column selection
        df = df.loc[:, ["Team", stat_col]].copy()

        df.columns = ["Team", label]

        # FIX: eliminate SettingWithCopyWarning
        df.loc[:, "Team"] = df["Team"].str.strip()

        return df

    except Exception as e:
        st.write(f"{label} → ERROR: {e}")
        return None

# ----------------------------------------------------
# STABLE STAT LIST (24 WORKING URLS)
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

# After spinner finishes
if team_stats is None or team_stats.empty:
    st.error("No valid TeamRankings tables were loaded.")
    st.stop()

#st.success("TeamRankings data loaded successfully!")

team_stats_dict = team_stats.set_index("Team").to_dict(orient="index")
# ----------------------------------------------------
# MATCHUP + MARKET
# ----------------------------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="tournament-header">MATCHUP</div>', unsafe_allow_html=True)

    team_a = st.selectbox("Home Team", list(team_stats_dict.keys()), key="team_a")
    team_b = st.selectbox("Away Team", list(team_stats_dict.keys()), key="team_b")

with col_right:
    
    st.markdown('<div class="tournament-header">MARKET ODDS</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Point Spread</div>
        </div>
    """, unsafe_allow_html=True)
    market_spread = st.number_input(" ", value=0.0, step=0.5, key="market_spread")

    st.markdown("""
        <div class="metric-card" style="margin-top: 1rem;">
            <div class="metric-label">Game Total</div>

        </div>
    """, unsafe_allow_html=True)
    market_total = st.number_input("  ", value=145.5, step=0.5, key="market_total")

    st.markdown("</div>", unsafe_allow_html=True)
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
# SIM DEFAULTS (before sliders overwrite them)
# ----------------------------------------------------
sigma = 12.0
num_sims = 14000

# ----------------------------------------------------
# SIMULATION SETTINGS (COLLAPSIBLE)
# ----------------------------------------------------
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

    # ----------------------------------------------------
    # PROJECTION PANEL
    # ----------------------------------------------------
    st.markdown('<div class="tournament-header">SCOREBOARD PROJECTIONS</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Projected Score</div>
                <div class="metric-value">{proj_a:.1f}</div>
                <div class="metric-sub">{team_a}</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Projected Score</div>
                <div class="metric-value">{proj_b:.1f}</div>
                <div class="metric-sub">{team_b}</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Projected Total</div>
                <div class="metric-value">{proj_total:.1f}</div>
            </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # SIMULATION SUMMARY (HORIZONTAL)
    # ----------------------------------------------------
    st.markdown('<div class="tournament-header">SIMULATION SUMMARY</div>', unsafe_allow_html=True)

    ss1, ss2, ss3 = st.columns(3)

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


    # ----------------------------------------------------
    # MODEL VS MARKET
    # ----------------------------------------------------
    st.markdown('<div class="tournament-header">MODEL vs MARKET</div>', unsafe_allow_html=True)


    spread_edge_class = "edge-green" if spread_edge > 0 else "edge-red"
    total_edge_class  = "edge-green" if total_edge > 0 else "edge-red"

    mv1, mv2 = st.columns(2)

    with mv1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Spread Edge</div>
                <div class="metric-value {spread_edge_class}">{spread_edge:+.1f}</div>
                <div class="metric-sub">Market: {market_spread:+.1f}</div>
            </div>
        """, unsafe_allow_html=True)

    with mv2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Edge</div>
                <div class="metric-value {total_edge_class}">{total_edge:+.1f}</div>
                <div class="metric-sub">Market: {market_total:.1f}</div>
            </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# RIGHT COLUMN (optional)
# ----------------------------------------------------
with col_side:
    # You can put matchup info, market info, team logos, etc.
    pass

















































