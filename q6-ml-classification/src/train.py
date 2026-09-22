from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report


NUMERICAL_FEATURES = [
    "Age",
    "income",
    "number_of_logins",
    "purchase_count",
    "last_login_days",
]

CATEGORICAL_FEATURES = [
    "subscription",
]

TARGET_COLUMN = "will_churn"


def load_data(file_path):
    """Load and perform initial cleaning on customer dataset."""
    df = pd.read_csv(file_path)
    # Remove exact duplicate rows
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def build_pipeline():
    """Construct an end-to-end scikit-learn preprocessing and modeling pipeline."""
    # Numerical preprocessing: Median imputation + Standard scaling
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    # Categorical preprocessing: Mode imputation + One-hot encoding
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, NUMERICAL_FEATURES),
            ("cat", cat_pipeline, CATEGORICAL_FEATURES),
        ]
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(random_state=42, max_iter=1000)),
    ])

    return pipeline


def train_and_evaluate(data_path):
    """Run full ML workflow: loading, split, training, and evaluation."""
    df = load_data(data_path)

    # Separate features and target
    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET_COLUMN].astype(int)

    # Stratified train/test split (80/20) to maintain class ratio
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Build and fit pipeline (fitted only on training data to prevent data leakage)
    model = build_pipeline()
    model.fit(X_train, y_train)

    # Generate predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Compute evaluation metrics
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    test_prec = precision_score(y_test, y_test_pred, zero_division=0)
    test_rec = recall_score(y_test, y_test_pred, zero_division=0)
    report = classification_report(y_test, y_test_pred, zero_division=0)

    results = {
        "model": model,
        "train_accuracy": round(train_acc, 4),
        "test_accuracy": round(test_acc, 4),
        "test_precision": round(test_prec, 4),
        "test_recall": round(test_rec, 4),
        "classification_report": report,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
    }

    return results


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    dataset_path = current_dir.parent / "data" / "churn_data.csv"

    print("--- Training Logistic Regression Churn Classifier ---")
    results = train_and_evaluate(dataset_path)

    print(f"\nDataset Splits:")
    print(f"  Training samples : {results['train_samples']}")
    print(f"  Testing samples  : {results['test_samples']}")

    print(f"\nModel Performance Metrics (Unseen Test Set):")
    print(f"  Accuracy  : {results['test_accuracy'] * 100:.2f}%")
    print(f"  Precision : {results['test_precision'] * 100:.2f}%")
    print(f"  Recall    : {results['test_recall'] * 100:.2f}%")

    print(f"\nOverfitting Check:")
    print(f"  Train Accuracy : {results['train_accuracy'] * 100:.2f}%")
    print(f"  Test Accuracy  : {results['test_accuracy'] * 100:.2f}%")
    acc_diff = abs(results['train_accuracy'] - results['test_accuracy'])
    print(f"  Difference     : {acc_diff * 100:.2f}%")

    if acc_diff < 0.08:
        print("  Status: No significant overfitting observed (Train and Test performance are closely aligned).")
    else:
        print("  Status: Noticeable performance gap; inspect model complexity or regularization.")

    print(f"\nDetailed Classification Report:\n{results['classification_report']}")
