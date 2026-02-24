import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from ml.feature_engineering import build_features

def train_model(df):
    df = build_features(df)

    X = df[["spread_home", "spread_away", "total_points"]]
    y = df["market_wrong"]  # label you will define

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)

    joblib.dump(model, "ml/model.pkl")
    return model
