"""
Loan approval prediction using logistic regression model (83% accuracy).
Expects Backend/models/loan_model.pkl (or logistic_regression_model.pkl from LoanPrediction.ipynb).
"""
import os
import re
import joblib
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Feature order must match training: Gender, Married, Dependents, Education, Self_Employed,
# ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area
LOAN_FEATURE_ORDER = [
    "Gender", "Married", "Dependents", "Education", "Self_Employed",
    "ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term",
    "Credit_History", "Property_Area",
]

# Minimum required to make a prediction (numeric + credit history)
REQUIRED_LOAN_FIELDS = [
    "ApplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
]

# User-facing names and short descriptions for data collection
LOAN_FIELD_PROMPTS = {
    "ApplicantIncome": "your annual applicant income ($)",
    "CoapplicantIncome": "co-applicant income ($), or 0 if none",
    "LoanAmount": "loan amount you want ($)",
    "Loan_Amount_Term": "loan term in months (e.g. 360 for 30 years)",
    "Credit_History": "credit history: 1 for good, 0 for bad or unknown",
    "Gender": "Gender: Male or Female",
    "Married": "Married: Yes or No",
    "Dependents": "Number of dependents: 0, 1, 2, or 3",
    "Education": "Education: Graduate or Not Graduate",
    "Self_Employed": "Self-employed: Yes or No",
    "Property_Area": "Property area: Urban, Semiurban, or Rural",
}

MODEL_ACCURACY = 0.83  # 83%


def _model_path() -> Path:
    base = Path(__file__).resolve().parent
    models_dir = base / "models"
    for name in ("loan_model.pkl", "logistic_regression_model.pkl"):
        p = models_dir / name
        if p.exists():
            return p
    return models_dir / "loan_model.pkl"


_loan_model = None


def _load_model():
    global _loan_model
    if _loan_model is not None:
        return _loan_model
    path = _model_path()
    if not path.exists():
        return None
    try:
        _loan_model = joblib.load(path)
        return _loan_model
    except Exception:
        return None


def is_loan_related(message: str) -> bool:
    """True if the message is about loan approval or taking a loan."""
    t = message.lower().strip()
    return bool(
        re.search(r"\bloan\b", t)
        or re.search(r"\bborrow\b", t)
        or re.search(r"\btake\s+(a\s+)?loan\b", t)
        or re.search(r"\bget\s+(a\s+)?loan\b", t)
        or re.search(r"\bloan\s+approval\b", t)
        or re.search(r"\bshould\s+i\s+take\b", t)
        or "approval" in t
        or "how will i get the loan" in t
    )


def parse_loan_data_from_message(message: str) -> Dict[str, float]:
    """
    Extract loan-related numbers from natural language.
    Returns a dict with keys from LOAN_FEATURE_ORDER; missing values are absent.
    """
    text = message.strip()
    out = {}

    # Dollar amounts: "50000", "$50,000", "50k", "income 60000"
    def parse_amount(s: str) -> Optional[float]:
        s = s.replace(",", "").replace("$", "").strip()
        if not s:
            return None
        if s.lower().endswith("k"):
            return float(s[:-1]) * 1000
        try:
            return float(s)
        except ValueError:
            return None

    # Loan amount: "loan of 50000", "loan amount 50k", "50000 loan"
    for m in re.finditer(r"(?:loan\s*(?:amount|of)?|amount)\s*[:\s]*\$?\s*([\d,]+(?:\.\d+)?\s*k?)", text, re.I):
        val = parse_amount(m.group(1))
        if val is not None:
            out["LoanAmount"] = val / 1000.0  # model expects thousands
    if "LoanAmount" not in out:
        for m in re.finditer(r"\$?\s*([\d,]+(?:\.\d+)?)\s*k?\s*(?:loan|dollars?)", text, re.I):
            val = parse_amount(m.group(1) + ("k" if "k" in text[m.start():m.end() + 2].lower() else ""))
            if val is not None:
                out["LoanAmount"] = val / 1000.0
                break

    # Income: "income 60000", "60k income", "annual income 60000"
    for m in re.finditer(r"(?:applicant\s*)?(?:annual\s*)?income\s*[:\s]*\$?\s*([\d,]+(?:\.\d+)?\s*k?)", text, re.I):
        val = parse_amount(m.group(1))
        if val is not None:
            out["ApplicantIncome"] = val
    for m in re.finditer(r"(?:income|salary)\s*(?:is|of|=)\s*\$?\s*([\d,]+(?:\.\d+)?\s*k?)", text, re.I):
        val = parse_amount(m.group(1))
        if val is not None and "ApplicantIncome" not in out:
            out["ApplicantIncome"] = val

    # Coapplicant income
    for m in re.finditer(r"co[- ]?applicant\s*income\s*[:\s]*\$?\s*([\d,]+(?:\.\d+)?\s*k?)", text, re.I):
        val = parse_amount(m.group(1))
        if val is not None:
            out["CoapplicantIncome"] = val
    if "CoapplicantIncome" not in out:
        out["CoapplicantIncome"] = 0.0

    # Term: "60 months", "term 360", "30 years" -> 360
    for m in re.finditer(r"(?:term|tenure)\s*[:\s]*(\d+)\s*(?:months?|years?)?", text, re.I):
        term = int(m.group(1))
        if "year" in text[m.start():m.end() + 10].lower():
            term = term * 12
        out["Loan_Amount_Term"] = float(term)
    for m in re.finditer(r"(\d+)\s*months?", text, re.I):
        out["Loan_Amount_Term"] = float(int(m.group(1)))
    for m in re.finditer(r"(\d+)\s*years?", text, re.I):
        out["Loan_Amount_Term"] = float(int(m.group(1)) * 12)

    # Credit: "credit 700", "credit score 700", "credit history good/bad", "credit 1"
    for m in re.finditer(r"credit\s*(?:score|history)?\s*[:\s]*(\d+)", text, re.I):
        score = int(m.group(1))
        out["Credit_History"] = 1.0 if score >= 650 else 0.0
    if re.search(r"credit\s*(?:is\s*)?good|credit\s*history\s*1", text, re.I):
        out["Credit_History"] = 1.0
    if re.search(r"credit\s*(?:is\s*)?bad|credit\s*history\s*0|no\s*credit", text, re.I):
        out["Credit_History"] = 0.0

    # Defaults for categoricals (model expects encoded numbers)
    if "Gender" not in out:
        out["Gender"] = 1  # Male
    if "Married" not in out:
        out["Married"] = 0  # No
    if "Dependents" not in out:
        out["Dependents"] = 0
    if "Education" not in out:
        out["Education"] = 0  # Graduate
    if "Self_Employed" not in out:
        out["Self_Employed"] = 0  # No
    if "Property_Area" not in out:
        out["Property_Area"] = 2  # Urban

    return out


def has_sufficient_loan_data(data: Dict[str, float]) -> bool:
    """Check if we have the minimum required fields for prediction."""
    for key in REQUIRED_LOAN_FIELDS:
        if key not in data or data[key] is None:
            return False
        try:
            v = float(data[key])
            if key == "Credit_History" and v not in (0, 1):
                return False
        except (TypeError, ValueError):
            return False
    return True


def get_required_loan_fields_message() -> str:
    """Return a user-facing message listing what data is needed."""
    parts = [
        "To assess your loan, I need the following (reply in one message, e.g. 'Income 60000, loan amount 50000, term 60 months, credit good'):",
        "",
        "• **Applicant income** – your annual income in $",
        "• **Loan amount** – how much you want to borrow in $",
        "• **Loan term** – in months (e.g. 60 for 5 years, 360 for 30 years)",
        "• **Credit history** – good (1) or bad / unknown (0), or your credit score (e.g. 700)",
        "",
        "Optional: co-applicant income ($), number of dependents (0–3), married (yes/no), property area (urban/semiurban/rural).",
    ]
    return "\n".join(parts)


def build_feature_vector(data: Dict[str, float]) -> Optional[np.ndarray]:
    """Build feature array in model order; returns None if missing required."""
    arr = []
    for key in LOAN_FEATURE_ORDER:
        if key not in data:
            if key in REQUIRED_LOAN_FIELDS:
                return None
            if key == "CoapplicantIncome":
                arr.append(0.0)
            elif key == "Gender":
                arr.append(1)
            elif key == "Married":
                arr.append(0)
            elif key == "Dependents":
                arr.append(0)
            elif key == "Education":
                arr.append(0)
            elif key == "Self_Employed":
                arr.append(0)
            elif key == "Property_Area":
                arr.append(2)
            else:
                return None
        else:
            arr.append(float(data[key]))
    return np.array([arr])


def predict_loan_approval(data: Dict[str, float]) -> Optional[Tuple[bool, float]]:
    """
    Run the logistic regression model. Returns (approved: bool, confidence: float) or None if model missing / error.
    """
    model = _load_model()
    if model is None:
        return None
    if not has_sufficient_loan_data(data):
        return None
    X = build_feature_vector(data)
    if X is None:
        return None
    try:
        pred = model.predict(X)[0]
        # Loan_Status: Y=approved, N=rejected (often encoded as 1/0)
        approved = int(pred) == 1 if hasattr(pred, "__int__") else str(pred).upper() in ("Y", "1", "YES")
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)[0]
            confidence = float(max(proba))
        else:
            confidence = MODEL_ACCURACY
        return (approved, confidence)
    except Exception:
        return None


def loan_assessment_reply(message: str, collected_data: Optional[Dict[str, float]] = None) -> Tuple[str, bool]:
    """
    Main entry: parse message (and optional collected_data), run model or ask for data.
    Returns (reply_text, sufficient_data_used).
    """
    data = dict(collected_data) if collected_data else {}
    parsed = parse_loan_data_from_message(message)
    for k, v in parsed.items():
        if k not in data or data[k] is None:
            data[k] = v

    if not has_sufficient_loan_data(data):
        return (get_required_loan_fields_message(), False)

    result = predict_loan_approval(data)
    if result is None:
        # Model file missing or prediction failed
        if _load_model() is None:
            return (
                "The loan approval model (loan_model.pkl) is not found in Backend/models/. "
                "Please add the trained logistic regression model to enable predictions. "
                "Until then, you can share your income, loan amount, term, and credit history and I'll ask for the same for when the model is available.",
                False,
            )
        return (
            "Insufficient data. I need your applicant income ($), loan amount ($), loan term (months), and credit history (good=1, bad=0 or your score). "
            "Please provide these so I can run the loan approval model.",
            False,
        )
    approved, confidence = result
    pct = round(confidence * 100)
    model_note = f" (model accuracy: {int(MODEL_ACCURACY * 100)}%)"
    if approved:
        return (
            f"I am **{pct}%** confident that you **should take** this loan.{model_note} "
            "This is not financial advice; please confirm terms with your lender.",
            True,
        )
    return (
        f"I am **{pct}%** confident that you **should not take** this loan based on the data provided.{model_note} "
        "Consider improving your profile or discussing alternatives with your lender.",
        True,
    )
