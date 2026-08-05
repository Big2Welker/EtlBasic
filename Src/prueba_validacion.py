from extract import (
    extract_all_transactions,
    extract_reference_tables
)

from clean import clean_transactions
from transform import transform_transactions
from validate import validate_transactions

DATA_DIR = "../data/raw"

# Extracción
transactions = extract_all_transactions(DATA_DIR)

products, stores, promotions, monthly_targets = (
    extract_reference_tables(DATA_DIR)
)

# Limpieza
transactions = clean_transactions(transactions)

# Transformación
transactions = transform_transactions(
    transactions,
    products,
    stores,
    promotions,
    monthly_targets
)

# Validación
validate_transactions(transactions)