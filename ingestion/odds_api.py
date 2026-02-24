import requests
import pandas as pd

API_KEY = "c9b3a4bae45d5ee9d18bdd1f84fb3d4c"

def fetch_ncaab_odds():
    url = (
        "https://api.the-odds-api.com/v4/sports/basketball_ncaab/odds/"
        f"?apiKey={API_KEY}&regions=us&markets=h2h,spreads,totals&oddsFormat=american"
    )

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    rows = []

    for event in data:
        event_id = event.get("id")
        home = event.get("home_team")
        away = event.get("away_team")
        commence = event.get("commence_time")

        for book in event.get("bookmakers", []):
            book_name = book.get("title")
            last_update = book.get("last_update")

            markets = {m["key"]: m for m in book["markets"]}

            # Moneyline
            ml_home = ml_away = None
            if "h2h" in markets:
                for o in markets["h2h"]["outcomes"]:
                    if o["name"] == home:
                        ml_home = o["price"]
                    elif o["name"] == away:
                        ml_away = o["price"]

            # Spread
            spread_home = spread_away = None
            if "spreads" in markets:
                for o in markets["spreads"]["outcomes"]:
                    if o["name"] == home:
                        spread_home = o["point"]
                    elif o["name"] == away:
                        spread_away = o["point"]

            # Total
            total_points = total_over = total_under = None
            if "totals" in markets:
                total_points = markets["totals"]["outcomes"][0]["point"]
                for o in markets["totals"]["outcomes"]:
                    if o["name"] == "Over":
                        total_over = o["price"]
                    elif o["name"] == "Under":
                        total_under = o["price"]

            rows.append({
                "event_id": event_id,
                "commence_time": commence,
                "home_team": home,
                "away_team": away,
                "bookmaker": book_name,
                "last_update": last_update,
                "ml_home": ml_home,
                "ml_away": ml_away,
                "spread_home": spread_home,
                "spread_away": spread_away,
                "total_points": total_points,
                "total_over": total_over,
                "total_under": total_under
            })

    return pd.DataFrame(rows)
