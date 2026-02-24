# ingestion/odds_api.py

import requests
import pandas as pd
from utils.team_normalization import normalize_team_name

ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/basketball_ncaab/odds"
ODDS_API_KEY = "c9b3a4bae45d5ee9d18bdd1f84fb3d4c"   # Replace with your key or environment variable


def fetch_ncaab_odds() -> pd.DataFrame:
    """
    Fetch live NCAAB odds and return a clean, normalized DataFrame.

    Output columns:
      - game_id
      - home_team
      - away_team
      - spread_home
      - spread_away
      - total_points
      - book
    """

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "spreads,totals",
        "oddsFormat": "american",
    }

    resp = requests.get(ODDS_API_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    rows = []

    for game in data:
        home = normalize_team_name(game["home_team"])
        away = normalize_team_name(game["away_team"])

        if not game.get("bookmakers"):
            continue

        book = game["bookmakers"][0]
        book_name = book.get("title", "unknown")

        spread_home = None
        spread_away = None
        total_points = None

        for market in book.get("markets", []):
            if market["key"] == "spreads":
                for outcome in market["outcomes"]:
                    name = normalize_team_name(outcome["name"])
                    if name == home:
                        spread_home = outcome.get("point")
                    elif name == away:
                        spread_away = outcome.get("point")

            elif market["key"] == "totals":
                for outcome in market["outcomes"]:
                    total_points = outcome.get("point")

        rows.append(
            {
                "game_id": game.get("id", ""),
                "home_team": home,
                "away_team": away,
                "spread_home": spread_home,
                "spread_away": spread_away,
                "total_points": total_points,
                "book": book_name,
            }
        )

    return pd.DataFrame(rows)
)
