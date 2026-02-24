# ml_engine/predict.py

import joblib
import pandas as pd
from ml_engine.feature_engineering import build_features

MODEL_PATH = "ml_engine/model.pkl"


def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None


def predict_edges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the trained model to a merged odds+stats DataFrame.

    Steps:
      1. Build features
      2. If model exists, compute edge from predicted probability
      3. If no model, return df with ml_edge = 0.0

    Expects df to have at least:
      - spread_home
      - spread_away
      - total_points
    """

    df = build_features(df)
    model = load_model()

    if model is None:
        df["ml_edge"] = 0.0
        return df

    feature_cols = ["spread_home", "spread_away", "total_points", "spread_diff", "total_scaled", "off_eff_diff"]
    X = df[feature_cols]

    # Example: edge = P(market_wrong=1) - 0.5
    proba = model.predict_proba(X)[:, 1]
    df["ml_edge"] = proba - 0.5

    return df
