import joblib
from ml_engine.feature_engineering import build_features

MODEL_PATH = "ml_engine/model.pkl"

def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except:
        return None


def predict_edges(df):
    """
    Apply ML model to compute edges.
    If model doesn't exist yet, return df unchanged.
    """

    model = load_model()
    df = build_features(df)

    if model is None:
        # No model yet — return df with placeholder edge
        df["ml_edge"] = 0.0
        return df

    X = df[["spread_home", "spread_away", "total_points"]]
    df["ml_edge"] = model.predict_proba(X)[:, 1] - 0.5

    return df
