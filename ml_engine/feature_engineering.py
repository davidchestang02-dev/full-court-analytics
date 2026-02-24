# ml_engine/feature_engineering.py

import pandas as pd
from utils.team_normalization import normalize_team_name


def merge_odds_and_stats(odds_df: pd.DataFrame, stats_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge sportsbook odds with team stats using canonical team names.

    Expects:
      odds_df columns:
        - home_team
        - away_team
        - spread_home
        - spread_away
        - total_points
      stats_df columns:
        - Team (canonical, already normalized via normalize_team_name)
        - other stat columns

    Returns:
      One row per game with home_* and away_* stat columns attached.
    """

    odds = odds_df.copy()
    stats = stats_df.copy()

    # Ensure odds team names are normalized as well
    odds["home_team_norm"] = odds["home_team"].apply(normalize_team_name)
    odds["away_team_norm"] = odds["away_team"].apply(normalize_team_name)

    # Home merge
    home_stats = stats.add_prefix("home_")
    merged = odds.merge(
        home_stats,
        left_on="home_team_norm",
        right_on="home_Team",
        how="left",
    )

    # Away merge
    away_stats = stats.add_prefix("away_")
    merged = merged.merge(
        away_stats,
        left_on="away_team_norm",
        right_on="away_Team",
        how="left",
    )

    return merged


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build model-ready features from merged odds + stats.

    Assumes df already has:
      - spread_home
      - spread_away
      - total_points
      - home_* stat columns
      - away_* stat columns

    Adds:
      - spread_diff
      - total_scaled
      - (placeholder) market_wrong label if not present
    """

    df = df.copy()

    # Core numeric features from odds
    df["spread_diff"] = df["spread_home"] - df["spread_away"]
    df["total_scaled"] = df["total_points"] / 100.0

    # Example stat-based features (safe: use .get with fillna)
    # You can expand this with your favorite TR stats.
    if "home_offensive_efficiency" in df.columns and "away_offensive_efficiency" in df.columns:
        df["off_eff_diff"] = (
            df["home_offensive_efficiency"] - df["away_offensive_efficiency"]
        )
    else:
        df["off_eff_diff"] = 0.0

    # Placeholder label if not already defined
    if "market_wrong" not in df.columns:
        df["market_wrong"] = 0  # you’ll replace this with real label logic for training

    return df
