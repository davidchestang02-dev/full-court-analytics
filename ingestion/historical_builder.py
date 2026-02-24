# ingestion/historical_builder.py

import pandas as pd
from ingestion.odds_api import fetch_ncaab_odds
from ingestion.stats_api import fetch_team_stats
from ml_engine.feature_engineering import merge_odds_and_stats


def build_historical_dataset(odds_source: str | None = None) -> pd.DataFrame:
    if odds_source:
        odds_df = pd.read_csv(odds_source)
    else:
        odds_df = fetch_ncaab_odds()

    stats_df = fetch_team_stats()
    merged = merge_odds_and_stats(odds_df, stats_df)

    return merged

