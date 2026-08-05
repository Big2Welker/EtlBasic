

from extract import extract_all_transactions


DATA_DIR = "../data/raw"


df = extract_all_transactions(DATA_DIR)

print("\n========== EXTRACCIÓN COMPLETADA ==========\n")

print("Cantidad de filas:", len(df))
print("Cantidad de columnas:", len(df.columns))

print("\nColumnas:")
print(df.columns.tolist())

print("\nPrimeras 10 filas:")
print(df.head(10))

print("\nTipos de datos:")
print(df.dtypes)