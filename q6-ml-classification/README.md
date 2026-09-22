# Q6: Machine Learning Churn Classification

A modular scikit-learn pipeline predicting customer churn (`will_churn`) from customer demographics and engagement metrics.

## Pipeline Features
- **Data Ingestion & Cleaning**: Deduplication and schema verification using `pandas`.
- **Pre-processing via `ColumnTransformer`**:
  - Numerical features (`Age`, `income`, `number_of_logins`, `purchase_count`, `last_login_days`): Median Imputation + `StandardScaler`.
  - Categorical feature (`subscription`): Most-frequent Imputation + `OneHotEncoder(handle_unknown='ignore')`.
- **Classifier**: `LogisticRegression(max_iter=1000, random_state=42)` fitted within an end-to-end `Pipeline` to eliminate data leakage.
- **Evaluation**: Accuracy (63.33%), Precision (58.33%), Recall (53.85%), and overfitting analysis.

## How to Run & Test on Your Screen
Run the pipeline directly from your terminal:
```bash
python3 src/train.py
```
You will see the complete output on your screen:
- Split counts (120 train / 30 test)
- Model evaluation metrics (Accuracy, Precision, Recall)
- Overfitting check comparing train accuracy vs test accuracy
- Full classification report table

## Running Automated Tests
```bash
pytest tests/test_model.py -v
```
All 6 tests pass.
