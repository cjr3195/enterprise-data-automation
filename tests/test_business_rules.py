import pandas as pd

from src.business_rules import evaluate_record


# ============================================================
# TEST CONFIGURATION
# ============================================================

TEST_DATE = pd.Timestamp(
    "2026-06-15"
)


# ============================================================
# TEST DATA FACTORY
# ============================================================

def create_test_record(**overrides):
    """
    Create a valid base record for business-rule testing.

    Individual tests override only the fields required
    for the scenario being validated.
    """

    record = {
        "customer_id": "C90001",
        "customer_name": "TEST MEDICAL CENTER",
        "customer_type": "HCO",
        "state": "FL",
        "status": "ACTIVE",
        "contract_id": "CT90001",
        "contract_type": "STANDARD",
        "start_date": pd.Timestamp(
            "2026-01-01"
        ),
        "end_date": pd.Timestamp(
            "2026-12-31"
        ),
        "priority_level": "NORMAL",
    }

    record.update(
        overrides
    )

    return pd.Series(
        record
    )


# ============================================================
# STANDARD CONTRACT
# ============================================================

def test_standard_valid_contract():
    """
    Active customer with a valid standard contract
    should receive STANDARD classification.
    """

    row = create_test_record()

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "STANDARD"
    )

    assert (
        result["rule_applied"]
        == "STANDARD_VALID_CONTRACT"
    )


# ============================================================
# HIGH PRIORITY CONTRACT
# ============================================================

def test_high_priority_contract():
    """
    Valid contract configured with HIGH priority
    should receive HIGH PRIORITY classification.
    """

    row = create_test_record(
        contract_type="PRIORITY",
        priority_level="HIGH",
    )

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "HIGH PRIORITY"
    )

    assert (
        result["rule_applied"]
        == "HIGH_PRIORITY_CONTRACT"
    )


# ============================================================
# MISSING CONTRACT
# ============================================================

def test_missing_contract():
    """
    Customer without a contract should be classified
    as an EXCEPTION.
    """

    row = create_test_record(
        contract_id=pd.NA,
        contract_type=pd.NA,
        start_date=pd.NaT,
        end_date=pd.NaT,
        priority_level=pd.NA,
    )

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "EXCEPTION"
    )

    assert (
        result["rule_applied"]
        == "MISSING_CONTRACT"
    )


# ============================================================
# INACTIVE CUSTOMER
# ============================================================

def test_inactive_customer():
    """
    Inactive customer should require business review.
    """

    row = create_test_record(
        status="INACTIVE"
    )

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "REVIEW"
    )

    assert (
        result["rule_applied"]
        == "INACTIVE_CUSTOMER"
    )


# ============================================================
# MISSING START DATE
# ============================================================

def test_missing_contract_start_date():
    """
    Missing contract start date should produce
    an exception.
    """

    row = create_test_record(
        start_date=pd.NaT
    )

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "EXCEPTION"
    )

    assert (
        result["rule_applied"]
        == "INVALID_CONTRACT_DATES"
    )


# ============================================================
# MISSING END DATE
# ============================================================

def test_missing_contract_end_date():
    """
    Missing contract end date should produce
    an exception.
    """

    row = create_test_record(
        end_date=pd.NaT
    )

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "EXCEPTION"
    )

    assert (
        result["rule_applied"]
        == "INVALID_CONTRACT_DATES"
    )


# ============================================================
# INVALID DATE RANGE
# ============================================================

def test_invalid_contract_date_range():
    """
    Contract start date cannot occur after end date.
    """

    row = create_test_record(
        start_date=pd.Timestamp(
            "2026-12-31"
        ),
        end_date=pd.Timestamp(
            "2026-01-01"
        ),
    )

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "EXCEPTION"
    )

    assert (
        result["rule_applied"]
        == "INVALID_DATE_RANGE"
    )


# ============================================================
# FUTURE CONTRACT
# ============================================================

def test_future_contract():
    """
    Contract starting after the evaluation date
    should require review.
    """

    row = create_test_record(
        start_date=pd.Timestamp(
            "2026-08-01"
        ),
        end_date=pd.Timestamp(
            "2027-07-31"
        ),
    )

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "REVIEW"
    )

    assert (
        result["rule_applied"]
        == "FUTURE_CONTRACT"
    )


# ============================================================
# EXPIRED CONTRACT
# ============================================================

def test_expired_contract():
    """
    Contract ending before the evaluation date
    should require review.
    """

    row = create_test_record(
        start_date=pd.Timestamp(
            "2025-01-01"
        ),
        end_date=pd.Timestamp(
            "2025-12-31"
        ),
    )

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "REVIEW"
    )

    assert (
        result["rule_applied"]
        == "EXPIRED_CONTRACT"
    )


# ============================================================
# MISSING PRIORITY RULE
# ============================================================

def test_missing_priority_rule():
    """
    Contract type without configured priority
    should produce an exception.
    """

    row = create_test_record(
        contract_type="SPECIAL",
        priority_level=pd.NA,
    )

    result = evaluate_record(
        row,
        as_of_date=TEST_DATE,
    )

    assert (
        result["classification"]
        == "EXCEPTION"
    )

    assert (
        result["rule_applied"]
        == "MISSING_PRIORITY_RULE"
    )
