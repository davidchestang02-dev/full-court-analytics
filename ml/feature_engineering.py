import pandas as pd
from utils.team_normalization import normalize_team_name

def merge_odds_and_stats(odds_df, stats_df):
    # Normalize names
    odds_df["home_team_norm"] = odds_df["home_team"].apply(normalize_team_name)
    odds_df["away_team_norm"] = odds_df["away_team"].apply(normalize_team_name)
    stats_df["School_norm"] = stats_df["School"].apply(normalize_team_name)

    # Merge stats for home team
    merged = odds_df.merge(
        stats_df,
        left_on="home_team_norm",
        right_on="School_norm",
        how="left",
        suffixes=("", "_home")
    )

    # Merge stats for away team
    merged = merged.merge(
        stats_df,
        left_on="away_team_norm",
        right_on="School_norm",
        how="left",
        suffixes=("", "_away")
    )

    return merged


def build_features(df):
    # Example features (expand later)
    df["spread_diff"] = df["spread_home"] - df["spread_away"]
    df["total_points"] = df["total_points"].astype(float)

    # Add more features as needed
    return df
 df
