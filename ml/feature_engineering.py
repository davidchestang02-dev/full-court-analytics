import pandas as pd

def build_features(df):
    # Example features
    df["spread_diff"] = df["spread_home"] - df["spread_away"]
    df["total_diff"] = df["total_over"] - df["total_under"]
    return df
