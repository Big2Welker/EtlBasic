import pandas as pd


# ============================================================
# REGLA 1
# ESTANDARIZAR IDS
# ============================================================

def standardize_ids(df):
    """
    Estandariza los valores de los IDs:
    - Elimina espacios en blanco.
    - Convierte a mayúsculas.
    """

    id_columns = [
        "sale_line_id",
        "store_id",
        "product_id"
    ]

    for column in id_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    return df


# ============================================================
# REGLA 2
# LIMPIEZA DE TEXTO
# ============================================================

def clean_text(df):
    """
    Elimina espacios y homologa mayúsculas/minúsculas
    en los textos.
    """

    df["payment_method"] = (
        df["payment_method"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    return df


# ============================================================
# REGLA 3
# INTERPRETAR FECHAS
# ============================================================

def parse_date(value):
    """
    Convierte los tres formatos de fecha del laboratorio
    a un único tipo datetime.

    Cali      -> YYYY-MM-DD
    Bogotá    -> DD/MM/YYYY
    Medellín  -> MM-DD-YYYY
    """

    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()

    try:

        # Bogotá
        if "/" in value:
            return pd.to_datetime(
                value,
                format="%d/%m/%Y",
                errors="coerce"
            )

        # Cali
        first_part = value.split("-")[0]

        if len(first_part) == 4:
            return pd.to_datetime(
                value,
                format="%Y-%m-%d",
                errors="coerce"
            )

        # Medellín
        return pd.to_datetime(
            value,
            format="%m-%d-%Y",
            errors="coerce"
        )

    except Exception:
        return pd.NaT


def clean_dates(df):
    """
    Convierte la columna sale_date al tipo datetime.
    """

    df["sale_date"] = df["sale_date"].apply(parse_date)

    return df


# ============================================================
# REGLA 4
# CONVERTIR CAMPOS NUMÉRICOS
# ============================================================

def clean_numeric(df):
    """
    Convierte quantity y unit_price a valores numéricos.
    """

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unit_price"] = (
        df["unit_price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.strip()
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    return df


# ============================================================
# REGLA 5
# ELIMINAR DUPLICADOS
# ============================================================

def remove_duplicates(df):
    """
    Conserva la primera ocurrencia válida
    de cada sale_line_id.
    """

    df = df.drop_duplicates(
        subset="sale_line_id",
        keep="first"
    )

    return df


# ============================================================
# REGLA 6
# ELIMINAR REGISTROS INVÁLIDOS
# ============================================================

def remove_invalid_records(df):
    """
    Elimina registros que no cumplen
    las reglas del laboratorio.
    """

    # Fechas inválidas
    df = df.dropna(
        subset=["sale_date"]
    )

    # Cantidad mayor que cero
    df = df[
        df["quantity"] > 0
    ]

    # Precio mayor que cero
    df = df[
        df["unit_price"] > 0
    ]

    return df


# ============================================================
# REGLA 7
# PROMOCIONES
# ============================================================

def clean_promotions(df):
    """
    Representa los códigos de promoción
    faltantes de manera consistente.
    """

    df["promotion_code"] = (
        df["promotion_code"]
        .replace(
            ["", "N/A"],
            pd.NA
        )
    )

    return df


# ============================================================
# PIPELINE DE LIMPIEZA
# ============================================================

def clean_transactions(df):
    """
    Ejecuta todas las reglas de limpieza
    definidas para la Actividad 5.
    """

    print("\n========== LIMPIEZA Y ARMONIZACIÓN ==========\n")

    initial_rows = len(df)

    df = standardize_ids(df)
    df = clean_text(df)
    df = clean_dates(df)
    df = clean_numeric(df)
    df = remove_duplicates(df)
    df = remove_invalid_records(df)
    df = clean_promotions(df)

    final_rows = len(df)

    print(f"Registros iniciales : {initial_rows}")
    print(f"Registros finales   : {final_rows}")
    print(f"Registros eliminados: {initial_rows-final_rows}")

    print("\nLimpieza finalizada correctamente.\n")

    return df