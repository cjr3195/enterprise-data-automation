import pandas as pd


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text_columns(dataframe, columns):
    """
    Normalize selected text columns.

    Values are stripped of leading/trailing spaces and
    converted to uppercase for consistent comparisons.
    """

    dataframe = dataframe.copy()

    for column in columns:

        if column in dataframe.columns:

            dataframe[column] = (
                dataframe[column]
                .astype("string")
                .str.strip()
                .str.upper()
            )

    return dataframe


# ============================================================
# DATE NORMALIZATION
# ============================================================

def normalize_contract_dates(contracts):
    """
    Convert contract date columns to datetime values.

    Invalid or missing dates are converted to NaT so they
    can be evaluated later by the validation layer.
    """

    contracts = contracts.copy()

    date_columns = [
        "start_date",
        "end_date",
    ]

    for column in date_columns:

        contracts[column] = pd.to_datetime(
            contracts[column],
            errors="coerce",
        )

    return contracts


# ============================================================
# CUSTOMER TRANSFORMATION
# ============================================================

def transform_customers(customers):
    """
    Normalize customer data before consolidation.
    """

    customers = customers.copy()

    customers = normalize_text_columns(
        customers,
        columns=[
            "customer_id",
            "customer_name",
            "customer_type",
            "state",
            "status",
        ],
    )

    return customers


# ============================================================
# CONTRACT TRANSFORMATION
# ============================================================

def transform_contracts(contracts):
    """
    Normalize contract data before consolidation.
    """

    contracts = contracts.copy()

    contracts = normalize_text_columns(
        contracts,
        columns=[
            "contract_id",
            "customer_id",
            "contract_type",
        ],
    )

    contracts = normalize_contract_dates(
        contracts
    )

    return contracts


# ============================================================
# PRIORITY RULE TRANSFORMATION
# ============================================================

def transform_priority_rules(priority_rules):
    """
    Normalize priority reference data.
    """

    priority_rules = priority_rules.copy()

    priority_rules = normalize_text_columns(
        priority_rules,
        columns=[
            "contract_type",
            "priority_level",
        ],
    )

    return priority_rules


# ============================================================
# DATA CONSOLIDATION
# ============================================================

def consolidate_data(
    customers,
    contracts,
    priority_rules,
):
    """
    Combine customers, contracts, and priority reference data
    into a single dataset used by downstream business rules.
    """

    consolidated = customers.merge(
        contracts,
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    consolidated = consolidated.merge(
        priority_rules,
        on="contract_type",
        how="left",
        validate="many_to_one",
    )

    return consolidated


# ============================================================
# PIPELINE ENTRY POINT
# ============================================================

def transform_source_data(source_data):
    """
    Transform and consolidate all source datasets.
    """

    customers = transform_customers(
        source_data["customers"]
    )

    contracts = transform_contracts(
        source_data["contracts"]
    )

    priority_rules = transform_priority_rules(
        source_data["priority_rules"]
    )

    consolidated = consolidate_data(
        customers=customers,
        contracts=contracts,
        priority_rules=priority_rules,
    )

    return consolidated
