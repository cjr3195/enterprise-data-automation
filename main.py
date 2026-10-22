from src.extract import load_source_data
from src.transform import transform_source_data
from src.business_rules import apply_business_rules
from src.validation import validate_dataset
from src.excel_generator import generate_excel_report


# ============================================================
# PIPELINE
# ============================================================

def run_pipeline():
    """
    Execute the complete enterprise data automation pipeline.

    Pipeline stages:
        1. Extract source data
        2. Transform and consolidate data
        3. Apply business rules
        4. Validate processed records
        5. Generate Excel report
    """

    print("=" * 60)
    print("ENTERPRISE DATA AUTOMATION")
    print("=" * 60)

    # --------------------------------------------------------
    # STEP 1: EXTRACT
    # --------------------------------------------------------

    print()
    print("[1/5] Loading source data...")

    source_data = load_source_data()

    print(
        f"      Customers: "
        f"{len(source_data['customers'])}"
    )

    print(
        f"      Contracts: "
        f"{len(source_data['contracts'])}"
    )

    print(
        f"      Priority rules: "
        f"{len(source_data['priority_rules'])}"
    )

    # --------------------------------------------------------
    # STEP 2: TRANSFORM
    # --------------------------------------------------------

    print()
    print(
        "[2/5] Transforming and consolidating data..."
    )

    transformed_data = transform_source_data(
        source
