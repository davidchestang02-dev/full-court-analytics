import pandas as pd
from ingestion.odds_api import fetch_ncaab_odds
from ingestion.stats_api import fetch_team_stats

def build_historical_dataset():
    odds = fetch_ncaab_odds()
    stats = fetch_team_stats()

    # TODO: merge odds + stats + results
    # TODO: compute labels (cover, over/under, market wrong)
    # TODO: save to data/processed/

    return odds, stats
