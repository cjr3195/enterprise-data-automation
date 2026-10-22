from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
REFERENCE_DATA_DIR = DATA_DIR / "reference"


CUSTOMERS_FILE = RAW_DATA_DIR / "customers.csv"
CONTRACTS_FILE = RAW_DATA_DIR / "contracts.csv"
PRIORITY_RULES_FILE = (
    REFERENCE_DATA_DIR / "priority_rules.csv"
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

CUSTOMER_COLUMNS = {
    "customer_id",
    "customer_name",
    "customer_type",
    "state",
    "status",
}

CONTRACT_COLUMNS = {
    "contract_id",
    "customer_id",
    "contract_type",
    "start_date",
    "end_date",
}

PRIORITY_RULE_COLUMNS = {
    "contract_type",
    "priority_level",
}


# ============================================================
# VALIDATION
# ============================================================

def validate_columns(
    dataframe,
    required_columns,
    dataset_name,
):
    """
    Validate that a dataset contains all required columns.
    """

    missing_columns = (
        required_columns
        - set(dataframe.columns)
    )

    if missing_columns:
        missing = ", ".join(
            sorted(missing_columns)
        )

        raise ValueError(
            f"{dataset_name} is missing required "
            f"columns: {missing}"
        )


# ============================================================
# DATA LOADERS
# ============================================================

def load_customers():
    """
    Load and validate the customer dataset.
    """

    customers = pd.read_csv(
        CUSTOMERS_FILE
    )

    validate_columns(
        customers,
        CUSTOMER_COLUMNS,
        "Customers dataset",
    )

    return customers


def load_contracts():
    """
    Load and validate the contract dataset.
    """

    contracts = pd.read_csv(
        CONTRACTS_FILE
    )

    validate_columns(
        contracts,
        CONTRACT_COLUMNS,
        "Contracts dataset",
    )

    return contracts


def load_priority_rules():
    """
    Load and validate the priority reference table.
    """

    priority_rules = pd.read_csv(
        PRIORITY_RULES_FILE
    )

    validate_columns(
        priority_rules,
        PRIORITY_RULE_COLUMNS,
        "Priority rules dataset",
    )

    return priority_rules


# ============================================================
# PIPELINE ENTRY POINT
# ============================================================

def load_source_data():
    """
    Load all source datasets required by the pipeline.
    """

    customers = load_customers()
    contracts = load_contracts()
    priority_rules = load_priority_rules()

    return {
        "customers": customers,
        "contracts": contracts,
        "priority_rules": priority_rules,
    }
