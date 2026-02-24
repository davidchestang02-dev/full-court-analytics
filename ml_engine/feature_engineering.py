import pandas as pd

def build_features(df):
    """
    Build model-ready features from merged odds + stats data.
    Assumes df already contains sportsbook odds and team stats.
    """

    # Basic sanity cleaning
    df = df.copy()

    # Example engineered features
    df["spread_diff"] = df["spread_home"] - df["spread_away"]
    df["total_scaled"] = df["total_points"] / 100.0

    # Label (placeholder — you can refine this)
    df["market_wrong"] = (df["ml_edge"] > 0).astype(int)

    return df


def merge_odds_and_stats(odds_df, stats_df):
    """
    Merge sportsbook odds with team stats.
    odds_df: must contain home_team, away_team, spread_home, total_points
    stats_df: must contain team-level stats
    """

    # Merge home stats
    merged = odds_df.merge(
        stats_df.add_prefix("home_"),
        left_on="home_team",
        right_on="home_Team",
        how="left"
    )

    # Merge away stats
    merged = merged.merge(
        stats_df.add_prefix("away_"),
        left_on="away_team",
        right_on="away_Team",
        how="left"
    )

    return merged
