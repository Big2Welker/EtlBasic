from extract import extract_all_transactions
from clean import clean_transactions

DATA_DIR = "../data/raw"

# Extraer datos
transactions = extract_all_transactions(DATA_DIR)

print("ANTES DE LIMPIAR")
print(transactions.info())

# Limpiar datos
transactions = clean_transactions(transactions)

print("\nDESPUÉS DE LIMPIAR")
print(transactions.info())

print("\nPrimeras filas:")
print(transactions.head())