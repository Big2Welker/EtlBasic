import pandas as pd


# ============================================================
# VALIDACIÓN 1
# sale_line_id único
# ============================================================

def validate_unique_sale_line_id(df):

    if df["sale_line_id"].duplicated().any():

        duplicated = df[df["sale_line_id"].duplicated()]

        raise ValueError(
            f"ERROR: Se encontraron {len(duplicated)} sale_line_id duplicados."
        )

    print("✓ sale_line_id es único")


# ============================================================
# VALIDACIÓN 2
# Llaves y fechas obligatorias
# ============================================================

def validate_required_fields(df):

    required = [
        "sale_line_id",
        "sale_date",
        "store_id",
        "product_id"
    ]

    missing = df[required].isnull().sum()

    if missing.sum() > 0:

        raise ValueError(
            f"ERROR: Existen valores nulos.\n{missing}"
        )

    print("✓ No existen valores nulos en los campos obligatorios")


# ============================================================
# VALIDACIÓN 3
# Valores positivos
# ============================================================

def validate_positive_values(df):

    numeric_columns = [
        "quantity",
        "unit_price",
        "gross_sales",
        "net_sales"
    ]

    for column in numeric_columns:

        if (df[column] <= 0).any():

            raise ValueError(
                f"ERROR: La columna '{column}' contiene valores no positivos."
            )

    print("✓ Todas las métricas numéricas son positivas")


# ============================================================
# VALIDACIÓN 4
# Productos existentes
# ============================================================

def validate_products(df):

    if df["product_name"].isnull().any():

        raise ValueError(
            "ERROR: Existen productos que no coinciden con el maestro."
        )

    print("✓ Todos los productos existen en el maestro")


# ============================================================
# VALIDACIÓN 5
# Tiendas existentes
# ============================================================

def validate_stores(df):

    if df["store_name"].isnull().any():

        raise ValueError(
            "ERROR: Existen tiendas que no coinciden con el maestro."
        )

    print("✓ Todas las tiendas existen en el maestro")


# ============================================================
# VALIDACIÓN 6
# net_sales
# ============================================================

def validate_net_sales(df):

    expected = (
        df["gross_sales"]
        - df["discount_amount"]
    )

    if not expected.round(2).equals(df["net_sales"].round(2)):

        raise ValueError(
            "ERROR: net_sales no coincide con gross_sales - discount_amount."
        )

    print("✓ net_sales fue calculado correctamente")


# ============================================================
# PIPELINE DE VALIDACIÓN
# ============================================================

def validate_transactions(df):

    print("\n========== VALIDACIÓN ==========\n")

    validate_unique_sale_line_id(df)

    validate_required_fields(df)

    validate_positive_values(df)

    validate_products(df)

    validate_stores(df)

    validate_net_sales(df)

    print("\nTodas las validaciones fueron superadas.\n")

    return True