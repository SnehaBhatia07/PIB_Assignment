import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

# Ensure q6-ml-classification root is in sys.path for package imports
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir.parent))

from src.train import (
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN,
    load_data,
    build_pipeline,
    train_and_evaluate,
)

DATA_PATH = current_dir.parent / "data" / "churn_data.csv"


def test_load_data_columns():
    df = load_data(DATA_PATH)
    expected_cols = set(NUMERICAL_FEATURES + CATEGORICAL_FEATURES + [TARGET_COLUMN])
    assert expected_cols.issubset(df.columns)
    assert len(df) > 0


def test_build_pipeline_structure():
    pipeline = build_pipeline()
    assert "preprocessor" in pipeline.named_steps
    assert "classifier" in pipeline.named_steps


def test_model_training_and_binary_predictions():
    df = load_data(DATA_PATH)
    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET_COLUMN].astype(int)

    pipeline = build_pipeline()
    pipeline.fit(X, y)

    preds = pipeline.predict(X)
    assert len(preds) == len(X)
    unique_preds = set(preds)
    assert unique_preds.issubset({0, 1})


def test_evaluation_metrics_generation():
    results = train_and_evaluate(DATA_PATH)

    assert "train_accuracy" in results
    assert "test_accuracy" in results
    assert "test_precision" in results
    assert "test_recall" in results

    for metric in ["train_accuracy", "test_accuracy", "test_precision", "test_recall"]:
        assert 0.0 <= results[metric] <= 1.0

    assert results["train_samples"] > 0
    assert results["test_samples"] > 0


def test_pipeline_handles_missing_values():
    df = load_data(DATA_PATH)
    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET_COLUMN].astype(int)

    pipeline = build_pipeline()
    pipeline.fit(X, y)

    sample_with_nans = pd.DataFrame([
        {
            "Age": np.nan,
            "income": 50000,
            "number_of_logins": np.nan,
            "purchase_count": 2,
            "last_login_days": np.nan,
            "subscription": None,
        }
    ])

    pred = pipeline.predict(sample_with_nans)
    assert len(pred) == 1
    assert pred[0] in [0, 1]


def test_pipeline_handles_unseen_categories():
    df = load_data(DATA_PATH)
    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET_COLUMN].astype(int)

    pipeline = build_pipeline()
    pipeline.fit(X, y)

    sample_unseen_cat = pd.DataFrame([
        {
            "Age": 35,
            "income": 70000,
            "number_of_logins": 12,
            "purchase_count": 5,
            "last_login_days": 10,
            "subscription": "Enterprise_Special",
        }
    ])

    pred = pipeline.predict(sample_unseen_cat)
    assert len(pred) == 1
    assert pred[0] in [0, 1]


if __name__ == "__main__":
    pytest.main([str(Path(__file__).resolve()), "-v"])
