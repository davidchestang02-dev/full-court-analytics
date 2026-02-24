import joblib
from ml.feature_engineering import build_features

model = joblib.load("ml/model.pkl")

def predict_edges(df):
    df = build_features(df)
    df["ml_edge"] = model.predict_proba(df)[:, 1]
    return df

