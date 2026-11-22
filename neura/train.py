from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "laptop_data_cleaned.csv"
MODEL_PATH = ROOT / "models" / "model.pkl"

CATEGORICAL = ["Company", "TypeName", "Cpu_brand", "Gpu_brand", "Os"]


def build_model() -> Pipeline:
    return Pipeline([
        ("prep", ColumnTransformer(
            [("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL)],
            remainder="passthrough",
        )),
        ("rf", RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_leaf=2,
            n_jobs=-1,
            random_state=42,
        )),
    ])


def main():
    print(f"Читаю данные: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    X, y = df.drop(columns="Price"), df["Price"]

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    model = build_model()
    model.fit(X_tr, y_tr)

    pred = model.predict(X_te)
    print(f"R2 (по log-цене): {r2_score(y_te, pred):.3f}")
    print(f"Средняя ошибка (MAE): {mean_absolute_error(np.exp(y_te), np.exp(pred)):,.0f}")

    # финальное обучение на всех данных
    model.fit(X, y)

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH, compress=3)
    print(f"Модель сохранена: {MODEL_PATH}")


if __name__ == "__main__":
    main()