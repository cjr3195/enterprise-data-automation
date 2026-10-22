from datetime import date

import pandas as pd


# ============================================================
# BUSINESS CLASSIFICATIONS
# ============================================================

CLASSIFICATION_STANDARD = "STANDARD"
CLASSIFICATION_HIGH_PRIORITY = "HIGH PRIORITY"
CLASSIFICATION_REVIEW = "REVIEW"
CLASSIFICATION_EXCEPTION = "EXCEPTION"


# ============================================================
# RECORD-LEVEL BUSINESS RULES
# ============================================================

def evaluate_record(row, as_of_date=None):
    """
    Evaluate a consolidated customer record and determine
    its business classification.

    Rules are evaluated in priority order so that critical
    exceptions are identified before lower-priority outcomes.
    """

    if as_of_date is None:
        as_of_date = pd.Timestamp(
            date.today()
        )

    # --------------------------------------------------------
    # RULE 1: CUSTOMER WITHOUT CONTRACT
    # --------------------------------------------------------

    if pd.isna(row["contract_id"]):

        return {
            "classification": CLASSIFICATION_EXCEPTION,
            "decision_reason": (
                "Customer does not have an associated contract."
            ),
            "rule_applied": "MISSING_CONTRACT",
        }

    # --------------------------------------------------------
    # RULE 2: INACTIVE CUSTOMER
    # --------------------------------------------------------

    if row["status"] != "ACTIVE":

        return {
            "classification": CLASSIFICATION_REVIEW,
            "decision_reason": (
                "Customer is not currently active."
            ),
            "rule_applied": "INACTIVE_CUSTOMER",
        }

    # --------------------------------------------------------
    # RULE 3: INVALID CONTRACT DATES
    # --------------------------------------------------------

    if (
        pd.isna(row["start_date"])
        or pd.isna(row["end_date"])
    ):

        return {
            "classification": CLASSIFICATION_EXCEPTION,
            "decision_reason": (
                "Contract contains missing or invalid dates."
            ),
            "rule_applied": "INVALID_CONTRACT_DATES",
        }

    # --------------------------------------------------------
    # RULE 4: INVALID CONTRACT DATE RANGE
    # --------------------------------------------------------

    if row["start_date"] > row["end_date"]:

        return {
            "classification": CLASSIFICATION_EXCEPTION,
            "decision_reason": (
                "Contract start date occurs after its end date."
            ),
            "rule_applied": "INVALID_DATE_RANGE",
        }

    # --------------------------------------------------------
    # RULE 5: CONTRACT NOT YET ACTIVE
    # --------------------------------------------------------

    if row["start_date"] > as_of_date:

        return {
            "classification": CLASSIFICATION_REVIEW,
            "decision_reason": (
                "Contract has not started yet."
            ),
            "rule_applied": "FUTURE_CONTRACT",
        }

    # -------
