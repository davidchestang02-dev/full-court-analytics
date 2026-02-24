import pandas as pd
import requests
from utils.team_normalization import normalize_team_name


STATS_URL = "https://www.teamrankings.com/ncaa-basketball/stat/offensive-efficiency?view=team"


def fetch_team_stats():
    """
    Fetch NCAA team stats from TeamRankings (or any HTML table source),
    normalize column names, normalize team names, and return a clean DataFrame.
    """

    # ---------------------------------------------------------
    # 1. Pull HTML tables
    # ---------------------------------------------------------
    try:
        tables = pd.read_html(STATS_URL)
    except Exception as e:
        raise RuntimeError(f"Failed to load stats table: {e}")

    # TeamRankings always puts the main stats table first
    df = tables[0]

    # ---------------------------------------------------------
    # 2. Standardize column names
    # ---------------------------------------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("%", "pct")
        .str.replace("/", "_")
        .str.lower()
    )

    # TeamRankings usually names the team column "team"
    # but we normalize it to "Team" for consistency
    if "team" in df.columns:
        df.rename(columns={"team": "Team"}, inplace=True)
    elif "school" in df.columns:
        df.rename(columns={"school": "Team"}, inplace=True)
    else:
        raise KeyError(f"Stats table missing a team column. Columns: {df.columns.tolist()}")

    # ---------------------------------------------------------
    # 3. Drop rows with missing team names
    # ---------------------------------------------------------
    df = df.dropna(subset=["Team"])

    # ---------------------------------------------------------
    # 4. Normalize team names for merging
    # ---------------------------------------------------------
    df["Team"] = df["Team"].apply(normalize_team_name)

    # ---------------------------------------------------------
    # 5. Ensure numeric columns are numeric
    # ---------------------------------------------------------
    for col in df.columns:
        if col != "Team":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------------------------------------------------------
    # 6. Final clean DataFrame
    # ---------------------------------------------------------
    return df
