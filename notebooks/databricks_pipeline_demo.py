# Databricks notebook source

# ============================================================
# ENTERPRISE DATA AUTOMATION
# DATABRICKS PIPELINE DEMO
# ============================================================

"""
Portfolio demonstration of migrating a local Python automation
workflow into a Databricks-oriented execution model.

Pipeline:

    Source Data
        ↓
    Extraction
        ↓
    Transformation
        ↓
    Business Rules
        ↓
    Validation
        ↓
    Excel Generation
        ↓
    Shared Output

The production system that inspired this demonstration is not
included in this repository.

All datasets and business scenarios used here are synthetic.
"""


# COMMAND ----------

# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import sys

import pandas as pd

from src.transform import transform_source_data
from src.business_rules import apply_business_rules
from src.validation import validate_dataset
from src.excel_generator import generate_excel_report


# COMMAND ----------

# ============================================================
# NOTEBOOK PARAMETERS
# ============================================================

dbutils.widgets.text(
    "input_root",
    "",
    "Input Root"
)

dbutils.widgets.text(
    "output_root",
    "",
    "Output Root"
)

input_root = dbutils.widgets.get(
    "input_root"
)

output_root = dbutils.widgets.get(
    "output_root"
)

print(
    "Input root:",
    input_root
)

print(
    "Output root:",
    output_root
)


# COMMAND ----------

# ============================================================
# PARAMETER VALIDATION
# ============================================================

if not input_root:

    raise ValueError(
        "input_root parameter is required."
    )

if not output_root:

    raise ValueError(
        "output_root parameter is required."
    )


# COMMAND ----------

# ============================================================
# SOURCE PATHS
# ============================================================

input_root_path = Path(
    input_root
)

output_root_path = Path(
    output_root
)

customers_file = (
    input_root_path
    / "raw"
    / "customers.csv"
)

contracts_file = (
    input_root_path
    / "raw"
    / "contracts.csv"
)

priority_rules_file = (
    input_root_path
    / "reference"
    / "priority_rules.csv"
)


# COMMAND ----------

# ============================================================
# DATA EXTRACTION
# ============================================================

print("=" * 60)
print("DATABRICKS PIPELINE")
print("=" * 60)

print()
print("[1/5] Loading source data...")

customers = pd.read_csv(
    customers_file
)

contracts = pd.read_csv(
    contracts_file
)

priority_rules = pd.read_csv(
    priority_rules_file
)

source_data = {
    "customers": customers,
    "contracts": contracts,
    "priority_rules": priority_rules,
}

print(
    "Customers:",
    len(customers)
)

print(
    "Contracts:",
    len(contracts)
)

print(
    "Priority rules:",
    len(priority_rules)
)


# COMMAND ----------

# ============================================================
# TRANSFORMATION
# ============================================================

print()
print(
    "[2/5] Transforming and consolidating data..."
)

transformed_data = transform_source_data(
    source_data
)

print(
    "Consolidated records:",
    len(transformed_data)
)


# COMMAND ----------

# ============================================================
# BUSINESS RULES
# ============================================================

print()
print(
    "[3/5] Applying business rules..."
)

evaluated_data = apply_business_rules(
    transformed_data
)

classification_counts = (
    evaluated_data[
        "classification"
    ]
    .value_counts()
    .to_dict()
)

for classification, count in (
    classification_counts.items()
):

    print(
        f"{classification}: {count}"
    )


# COMMAND ----------

# ============================================================
# DATA VALIDATION
# ============================================================

print()
print(
    "[4/5] Validating processed records..."
)

validated_data = validate_dataset(
    evaluated_data
)

validation_counts = (
    validated_data[
        "validation_status"
    ]
    .value_counts()
    .to_dict()
)

for status, count in (
    validation_counts.items()
):

    print(
        f"{status}: {count}"
    )


# COMMAND ----------

# ============================================================
# EXCEL OUTPUT
# ============================================================

print()
print(
    "[5/5] Generating Excel report..."
)

output_file = (
    output_root_path
    / "enterprise_automation_report.xlsx"
)

generated_file = generate_excel_report(
    validated_data,
    output_file=output_file,
)


# COMMAND ----------

# ============================================================
# PIPELINE SUMMARY
# ============================================================

print()
print("=" * 60)
print("DATABRICKS PIPELINE COMPLETED")
print("=" * 60)

print(
    "Records processed:",
    len(validated_data)
)

print(
    "Output:",
    generated_file
)


# COMMAND ----------

# ============================================================
# JOB OUTPUT VALUES
# ============================================================

try:

    dbutils.jobs.taskValues.set(
        key="records_processed",
        value=int(
            len(validated_data)
        ),
    )

    dbutils.jobs.taskValues.set(
        key="output_file",
        value=str(
            generated_file
        ),
    )

except Exception as error:

    print(
        "Task values were not recorded:",
        error
    )
