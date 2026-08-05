from extract import (
    extract_all_transactions,
    extract_reference_tables
)

from clean import clean_transactions
from transform import transform_transactions


DATA_DIR = "../data/raw"


# Extraer datos
transactions = extract_all_transactions(DATA_DIR)

products, stores, promotions, monthly_targets = (
    extract_reference_tables(DATA_DIR)
)

# Limpiar
transactions = clean_transactions(transactions)

# Transformar
transactions = transform_transactions(
    transactions,
    products,
    stores,
    promotions,
    monthly_targets
)

print(transactions.info())

print("\nPrimeras filas:")
print(transactions.head())