from extract import (
    extract_all_transactions,
    extract_reference_tables
)

from clean import clean_transactions
from transform import transform_transactions
from validate import validate_transactions
from load import load_data

DATA_DIR = "../data/raw"

# ===========================
# EXTRACCIÓN
# ===========================

transactions = extract_all_transactions(DATA_DIR)

products, stores, promotions, monthly_targets = (
    extract_reference_tables(DATA_DIR)
)

# ===========================
# LIMPIEZA
# ===========================

transactions = clean_transactions(transactions)

# ===========================
# TRANSFORMACIÓN
# ===========================

transactions = transform_transactions(
    transactions,
    products,
    stores,
    promotions,
    monthly_targets
)

# ===========================
# VALIDACIÓN
# ===========================

validate_transactions(transactions)

# ===========================
# CARGA
# ===========================

load_data(transactions)