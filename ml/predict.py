import joblib
import pandas as pd
from ml.feature_engineering import build_features

model = joblib.load("ml/model.pkl")

def predict(df):
    df = build_features(df)
    probs = model.predict_proba(df)[:, 1]
    df["ml_edge"] = probs
    return df
