import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def train():
    df = pd.read_csv("dataset.csv")
    df["Extracurricular Activities"] = LabelEncoder().fit_transform(
        df["Extracurricular Activities"]
    )
    x = df.drop("Performance Index", axis=1)
    y = df["Performance Index"]
    if len(df) < 2:
        print("Dataset too small to split; using entire dataset for training.")
        model = RandomForestRegressor(n_estimators=200, random_state=42)
        model.fit(x, y)
    else:
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )
        model = RandomForestRegressor(n_estimators=200, random_state=42)
        model.fit(x_train, y_train)
    joblib.dump(model, "performance/model.pkl")
    print("Model trained and saved")
