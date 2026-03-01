# Backend models

Place trained model files here so the Finance plugin can use them.

## Loan approval (83% accuracy)

- **`loan_model.pkl`** or **`logistic_regression_model.pkl`** – Logistic regression model from `Domain/Finance/Model/TrainTestCompare/LoanPrediction.ipynb`.
- Copy the saved file from the notebook output directory (e.g. `logistic_regression_model.pkl`) into this folder and optionally rename to `loan_model.pkl`.

The API will then:
- Activate the **Finance** plugin for loan-related questions.
- Ask for: applicant income, loan amount, loan term, credit history.
- Return: *"I am X% confident that you should [take / not take] this loan."*
- If the user cannot provide data: *"Insufficient data. Without the required information I cannot run the loan approval model."*

## Stock / investment

- **`stock_gb_model.pkl`** – Gradient Boosting model for stock movement.
- **`stock_scaler.pkl`** – Scaler for features (e.g. from `StockMarket.ipynb`).
- **`svm_model.pkl`** (optional) – SVM model for ensemble.

If only `stock_gb_model.pkl` and `stock_scaler.pkl` are present, the stock predictor still runs using the GB model. Investment-amount guidance uses portfolio risk logic and does not require these files.
