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

    # --------------------------------------------------------
    # RULE 6: EXPIRED CONTRACT
    # --------------------------------------------------------

    if row["end_date"] < as_of_date:

        return {
            "classification": CLASSIFICATION_REVIEW,
            "decision_reason": (
                "Contract has expired."
            ),
            "rule_applied": "EXPIRED_CONTRACT",
        }

    # --------------------------------------------------------
    # RULE 7: MISSING PRIORITY CONFIGURATION
    # --------------------------------------------------------

    if pd.isna(row["priority_level"]):

        return {
            "classification": CLASSIFICATION_EXCEPTION,
            "decision_reason": (
                "Contract type does not have a configured "
                "priority rule."
            ),
            "rule_applied": "MISSING_PRIORITY_RULE",
        }

    # --------------------------------------------------------
    # RULE 8: HIGH PRIORITY CONTRACT
    # --------------------------------------------------------

    if row["priority_level"] == "HIGH":

        return {
            "classification": CLASSIFICATION_HIGH_PRIORITY,
            "decision_reason": (
                "Customer is active and has a valid "
                "high-priority contract."
            ),
            "rule_applied": "HIGH_PRIORITY_CONTRACT",
        }

    # --------------------------------------------------------
    # RULE 9: STANDARD VALID CONTRACT
    # --------------------------------------------------------

    return {
        "classification": CLASSIFICATION_STANDARD,
        "decision_reason": (
            "Customer is active and has a valid "
            "standard contract."
        ),
        "rule_applied": "STANDARD_VALID_CONTRACT",
    }


# ============================================================
# DATASET-LEVEL RULE APPLICATION
# ============================================================

def apply_business_rules(
    dataframe,
    as_of_date=None,
):
    """
    Apply business rules to every record in the consolidated
    dataset.

    Returns the original dataset with classification,
    decision reason, and applied rule columns.
    """

    dataframe = dataframe.copy()

    rule_results = dataframe.apply(
        lambda row: evaluate_record(
            row,
            as_of_date=as_of_date,
        ),
        axis=1,
    )

    rule_results = pd.DataFrame(
        rule_results.tolist(),
        index=dataframe.index,
    )

    result = pd.concat(
        [
            dataframe,
            rule_results,
        ],
        axis=1,
    )

    return result
