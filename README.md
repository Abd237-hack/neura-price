# NEURA-PRICE

A laptop price estimator powered by a RandomForest model, with a pywebview desktop interface and a CLI version.

## What this tool does

You pick or enter a laptop's specs (brand, type, RAM, weight, display, CPU, GPU, storage, and OS), and it estimates the price based on historical data, converting the result into USD and TJS.

## Download

To run the app on Windows without setting up Python, download the latest zip from [Releases](https://github.com/Abd237-hack/neura-price/releases), extract it, and open `app.exe`.

## How to run from source

Make sure [uv](https://docs.astral.sh/uv/) is installed, then run:

```bash
uv sync
uv run python -m neura.train   # optional, retrains models/model.pkl
uv run python app.py           # desktop UI
uv run python cli.py           # terminal version


A quick note on accuracy
The model was trained on a 2018 Kaggle CSV dataset (prices in INR) that unfortunately isn't complete and misses newer hardware, so sorry in advance if the estimates feel off or undervalued for modern laptops. Currency conversion rates for USD and TJS are also hardcoded in neura/predictor.py. Test R² score on the dataset is 0.88.


