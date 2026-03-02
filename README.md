# Full Court Analytics

College basketball predictive engine built with Streamlit.

## What this build now supports

The app now runs a **5-layer automated projection pipeline** for daily NCAA Men's matchups:

1. **Deterministic model layer** (efficiency + pace + possession adjustments).
2. **Monte Carlo simulation layer** for outcome distributions and cover/total probabilities.
3. **Situational trend layer** (home edge, scoring margin, pace/shooting market trend proxies).
4. **Regression rebalance layer** that shrinks model output toward market-implied lines while using ML edge strength.
5. **Unified projection layer** that emits final score projection, spread/total edges, probabilities, and recommended side.

## ML refinement approach

- Existing model inference (`ml_engine/predict.py`) computes an `ml_edge` signal.
- That `ml_edge` is fed into the projection stack to rebalance how much trust goes to model vs market.
- As you add season-long historical labeled outcomes, retraining can continuously improve calibration.

## Current output for each game

- Projected score (home and away)
- Projected total and spread
- Cover and O/U probabilities
- Model-vs-market edge values
- Confidence score for action prioritization

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Important note on performance target

A 75% long-term hit rate against efficient betting markets is extremely difficult and should be treated as aspirational. Use robust backtesting, proper bankroll/risk controls, and periodic model recalibration before any live capital deployment.
