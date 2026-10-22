import pandas as pd


# ============================================================
# VALIDATION CONSTANTS
# ============================================================

VALIDATION_PASSED = "PASSED"
VALIDATION_WARNING = "WARNING"
VALIDATION_FAILED = "FAILED"


# ============================================================
# RECORD-LEVEL VALIDATION
# ============================================================

def validate_record(row):
    """
    Validate the data quality and integrity of a processed record.

    Validation is independent from the business classification.
    A record may require business review while still passing
    technical data-quality validation.
    """

    errors = []
    warnings = []

    # --------------------------------------------------------
    # CUSTOMER VALIDATION
    # --------------------------------------------------------

    if pd.isna(row["customer_id"]):
        errors.append(
            "Missing customer ID."
        )

    if pd.isna(row["customer_name"]):
        errors.append(
            "Missing customer name."
        )

    if pd.isna(row["customer_type"]):
        warnings.append(
            "Missing customer type."
        )

    if pd.isna(row["state"]):
        warnings.append(
            "Missing customer state."
        )

    if pd.isna(row["status"]):
        errors.append(
            "Missing customer status."
        )

    # --------------------------------------------------------
    # CONTRACT VALIDATION
    # --------------------------------------------------------

    has_contract = not pd.isna(
        row["contract_id"]
    )

    if has_contract:

        if pd.isna(row["contract_type"]):
            errors.append(
                "Contract exists but contract type is missing."
            )

        if pd.isna(row["start_date"]):
            errors.append(
                "Contract start date is missing or invalid."
            )

        if pd.isna(row["end_date"]):
            errors.append(
                "Contract end date is missing or invalid."
            )

        if (
            not pd.isna(row["start_date"])
            and not pd.isna(row["end_date"])
            and row["start_date"] > row["end_date"]
        ):
            errors.append(
                "Contract start date occurs after end date."
            )

    else:

        warnings.append(
            "Customer does not have an associated contract."
        )

    # --------------------------------------------------------
    # PRIORITY CONFIGURATION VALIDATION
    # --------------------------------------------------------

    if (
        has_contract
        and not pd.isna(row["contract_type"])
        and pd.isna(row["priority_level"])
    ):
        warnings.append(
            "Contract type does not have a configured "
            "priority level."
        )

    # --------------------------------------------------------
    # BUSINESS RULE OUTPUT VALIDATION
    # --------------------------------------------------------

    if pd.isna(row["classification"]):
        errors.append(
            "Business classification was not generated."
        )

    if pd.isna(row["rule_applied"]):
        errors.append(
            "Applied business rule was not recorded."
        )

    if pd.isna(row["decision_reason"]):
        errors.append(
            "Decision reason was not generated."
        )

    # --------------------------------------------------------
    # FINAL VALIDATION STATUS
    # --------------------------------------------------------

    if errors:

        validation_status = (
            VALIDATION_FAILED
        )

    elif warnings:

        validation_status = (
            VALIDATION_WARNING
        )

    else:

        validation_status = (
            VALIDATION_PASSED
        )

    all_issues = (
        errors
        + warnings
    )

    return {
        "validation_status": validation_status,
        "validation_issues": (
            " | ".join(all_issues)
            if all_issues
            else None
        ),
        "validation_error_count": len(
            errors
        ),
        "validation_warning_count": len(
            warnings
        ),
    }


# ============================================================
# DATASET-LEVEL VALIDATION
# ============================================================

def validate_dataset(dataframe):
    """
    Apply data-quality validation to every processed record.

    Returns the original dataset with validation status,
    issues, error count, and warning count.
    """

    dataframe = dataframe.copy()

    validation_results = dataframe.apply(
        validate_record,
        axis=1,
    )

    validation_results = pd.DataFrame(
        validation_results.tolist(),
        index=dataframe.index,
    )

    result = pd.concat(
        [
            dataframe,
            validation_results,
        ],
        axis=1,
    )

    return result
