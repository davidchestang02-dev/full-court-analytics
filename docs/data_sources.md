# NCAA Men's Basketball Data Sources (Team Stats + Sportsbook Markets)

This guide lists practical API/data providers you can use to power Full Court Analytics.

## 1) Sportsbook market odds (spreads, totals, moneylines)

### Option A: The Odds API (good starter)
- Website: https://the-odds-api.com/
- Coverage: US books, spreads/totals/moneyline, multiple sports including NCAAB.
- Pros: Easy REST API, broad bookmaker coverage, affordable to start.
- Cons: Historical depth is limited by plan; request quota matters.
- Good for: Daily automation + market consensus snapshots.

### Option B: OddsJam / OpticOdds / SportdataAPI / Goalserve (commercial feeds)
- Pros: Better coverage, often deeper markets and history, stronger uptime SLAs.
- Cons: Higher monthly cost and licensing complexity.
- Good for: Production subscription products where data reliability is critical.

### Option C: Direct sportsbook APIs (where allowed)
- Pros: Fastest/cleanest direct lines from a specific book.
- Cons: Usually no unified schema across books and legal/restriction concerns.
- Good for: Book-specific execution or arbitrage workflows.

## 2) Team stats + game results

### Option A: CollegeBasketballData API
- Website: https://www.collegebasketballdata.com/
- Coverage: NCAA teams, games, schedules, ratings-style info.
- Pros: College basketball specific and generally easier than scraping.
- Cons: Verify endpoint depth and historical limits for your use case.

### Option B: SportsDataIO (NCAA Basketball)
- Website: https://sportsdata.io/
- Coverage: Team/game stats, schedules, injuries/news in some tiers.
- Pros: Enterprise-friendly docs and consistency.
- Cons: Paid tiers can be expensive.

### Option C: Sportradar NCAA Basketball
- Website: https://developer.sportradar.com/
- Coverage: Deep official feeds.
- Pros: High quality and robust historical support.
- Cons: Enterprise pricing and contract process.

### Option D: Bart Torvik / KenPom-style sources (for advanced efficiency features)
- Great for efficiency signals, but licensing/access varies.
- Important: confirm ToS and commercial usage rights before product use.

## 3) Recommended architecture for your app

Use a **two-provider strategy**:
1. **Primary market feed** for odds (e.g., The Odds API to start).
2. **Primary stats/results feed** for team/game data (e.g., CollegeBasketballData or SportsDataIO).
3. Optional fallback provider for outage resilience.

Then normalize everything into your own canonical schema:
- `games` (game_id, date, home_team_id, away_team_id)
- `market_snapshots` (timestamp, bookmaker, spread_home, total, ml_home)
- `team_game_stats` (possessions, off_eff, def_eff, reb%, tov%, shot profile)
- `results` (final_home, final_away, closing_spread, closing_total)

## 4) What to collect daily (automation checklist)

- **Morning pull**: opening lines + baseline model run.
- **Intra-day pull**: line movement snapshots every 15–30 min.
- **Pre-tip pull**: closing lines (critical for model evaluation).
- **Postgame pull**: final scores + derived labels:
  - `market_wrong_spread`
  - `market_wrong_total`
  - ROI per signal bucket

## 5) Practical next step for this repo

Short-term implementation path:
1. Keep your current odds ingestion module and add a provider abstraction (`provider_name`, `fetched_at`, `bookmaker`).
2. Replace HTML scraping-heavy team stat flow with a stable API source where possible.
3. Build a historical warehouse table (CSV/DB) to support retraining + backtesting.
4. Add evaluation metrics:
   - ATS accuracy
   - O/U accuracy
   - CLV (closing line value)
   - ROI by confidence decile

## 6) Compliance and risk notes

- Ensure each data provider’s terms permit commercial/subscription use.
- Avoid unauthorized scraping for production use where prohibited.
- Betting products may require jurisdiction-specific legal disclosures.
- A sustained 75% win rate against efficient markets is rare; validate with strict out-of-sample backtests.
