from pathlib import Path

import joblib
import numpy as np
import pandas as pd

CATEGORICAL = ["Company", "TypeName", "Cpu_brand", "Gpu_brand", "Os"]
DEFAULT_MODEL = Path(__file__).resolve().parent.parent / "models" / "model.pkl"

DATASET_PER_USD = 82.0   # проверь, в какой валюте цены в CSV
TJS_PER_USD = 9.24


class Predictor:
    def __init__(self, path=DEFAULT_MODEL):
        self.model = joblib.load(path)
        enc = self.model.named_steps["prep"].named_transformers_["cat"]
        self.options = {c: sorted(cats) for c, cats in zip(CATEGORICAL, enc.categories_)}

    def predict(self, specs: dict) -> dict:
        price = float(np.exp(self.model.predict(pd.DataFrame([specs]))[0]))
        usd = price / DATASET_PER_USD
        return {"rub": price, "usd": usd, "tjs": usd * TJS_PER_USD}