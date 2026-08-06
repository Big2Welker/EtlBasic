import pandas as pd
from extract import extract_all_transactions


DATA_DIR = "../data/raw"


def profile_transactions(df):
    print("\n" + "=" * 60)
    print("PERFILAMIENTO DE DATOS - LAB 1B")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Dimensiones
    # --------------------------------------------------------
    print("\n1. DIMENSIONES")
    print("-" * 60)
    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")

    # --------------------------------------------------------
    # 2. Columnas
    # --------------------------------------------------------
    print("\n2. COLUMNAS")
    print("-" * 60)
    for column in df.columns:
        print(f"- {column}")

    # --------------------------------------------------------
    # 3. Tipos de datos
    # --------------------------------------------------------
    print("\n3. TIPOS DE DATOS")
    print("-" * 60)
    print(df.dtypes)

    # --------------------------------------------------------
    # 4. Valores faltantes
    # --------------------------------------------------------
    print("\n4. VALORES FALTANTES")
    print("-" * 60)

    missing = df.isnull().sum()

    for column, amount in missing.items():
        print(f"{column}: {amount}")
    # --------------------------------------------------------
    # 5. Sale_line_id duplicados
    # --------------------------------------------------------
    print("\n5. DUPLICADOS DE sale_line_id")
    print("-" * 60)

    # Obtiene todas las filas cuyo sale_line_id aparece más de una vez
    duplicated = df[df["sale_line_id"].duplicated(keep=False)]

    # Cuenta cuántos IDs están duplicados
    duplicated_ids = duplicated["sale_line_id"].nunique()

    print(f"Registros duplicados: {duplicated_ids}")

    if not duplicated.empty:
        print("\nRegistros encontrados:")

        print(
            duplicated[
                [
                    "sale_line_id",
                    "sale_date",
                    "store_id",
                    "product_id",
                    "quantity",
                    "unit_price",
                    "promotion_code",
                    "payment_method"
                ]
            ]
            .sort_values("sale_line_id")
            .to_string(index=False)
        )

    # --------------------------------------------------------
    # 6. Cantidades inválidas
    # --------------------------------------------------------
    print("\n6. CANTIDADES INVÁLIDAS")
    print("-" * 60)

    quantity_numeric = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    invalid_quantity = (
        quantity_numeric.isna()
        | (quantity_numeric <= 0)
    )

    print(f"Cantidad de registros inválidos: {invalid_quantity.sum()}")

    if invalid_quantity.sum() > 0:
        print("\nRegistros encontrados:")
        print(
            df.loc[
                invalid_quantity,
                ["sale_line_id", "quantity"]
            ]
        )

    # --------------------------------------------------------
    # 7. Precios inválidos
    # --------------------------------------------------------
    print("\n7. PRECIOS INVÁLIDOS")
    print("-" * 60)

    price_numeric = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    invalid_price = (
        price_numeric.isna()
        | (price_numeric <= 0)
    )

    print(f"Cantidad de registros inválidos: {invalid_price.sum()}")

    if invalid_price.sum() > 0:
        print("\nRegistros encontrados:")
        print(
            df.loc[
                invalid_price,
                ["sale_line_id", "unit_price"]
            ]
        )

    # --------------------------------------------------------
    # 8. Fechas inválidas
    # --------------------------------------------------------
    print("\n8. FECHAS INVÁLIDAS")
    print("-" * 60)

    dates = pd.to_datetime(
        df["sale_date"],
        errors="coerce",
        dayfirst=True
    )

    invalid_dates = dates.isna()

    print(f"Cantidad de fechas inválidas: {invalid_dates.sum()}")

    if invalid_dates.sum() > 0:
        print("\nRegistros encontrados:")
        print(
            df.loc[
                invalid_dates,
                ["sale_line_id", "sale_date"]
            ]
        )

    # --------------------------------------------------------
    # 9. Valores categóricos
    # --------------------------------------------------------
    print("\n9. VALORES CATEGÓRICOS")
    print("-" * 60)

    categorical_columns = [
        "store_id",
        "product_id",
        "promotion_code",
        "payment_method"
    ]

    for column in categorical_columns:
        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False))

    # --------------------------------------------------------
    # 10. Resumen general
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("PERFILAMIENTO FINALIZADO")
    print("=" * 60)


if __name__ == "__main__":

    transactions = extract_all_transactions(DATA_DIR)

    profile_transactions(transactions)