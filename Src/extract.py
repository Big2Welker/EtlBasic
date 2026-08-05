import pandas as pd
import xml.etree.ElementTree as ET
import json
import os


# ============================================================
# ESQUEMA COMÚN
# ============================================================

COMMON_COLUMNS = [
    "sale_line_id",
    "sale_date",
    "store_id",
    "product_id",
    "quantity",
    "unit_price",
    "promotion_code",
    "payment_method"
]


# ============================================================
# EXTRACCIÓN - CALI (CSV)
# ============================================================

def extract_cali_csv(file_path):
    """
    Extrae las transacciones de Cali desde CSV.

    En esta etapa NO se limpian ni transforman los datos.
    Solamente se garantiza el esquema común.
    """

    df = pd.read_csv(file_path)

    return df[COMMON_COLUMNS]


# ============================================================
# EXTRACCIÓN - BOGOTÁ (JSON)
# ============================================================

def extract_bogota_json(file_path):
    """
    Extrae las transacciones de Bogotá desde JSON
    y homologa los nombres de columnas al esquema común.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    # Homologación de nombres del JSON de Bogotá
    df = df.rename(columns={
        "id_linea": "sale_line_id",
        "fecha": "sale_date",
        "sucursal": "store_id",
        "codigo_producto": "product_id",
        "unidades": "quantity",
        "precio": "unit_price",
        "promocion": "promotion_code",
        "medio_pago": "payment_method"
    })

    return df[COMMON_COLUMNS]


# ============================================================
# EXTRACCIÓN - MEDELLÍN (XML)
# ============================================================

def extract_medellin_xml(file_path):
    """
    Extrae las transacciones de Medellín desde XML
    y las convierte al esquema común.
    """

    tree = ET.parse(file_path)
    root = tree.getroot()

    records = []

    # El XML real utiliza <sale>
    for elem in root.findall(".//sale"):

        records.append({
            "sale_line_id": (
                elem.findtext("line_id")
            ),

            "sale_date": (
                elem.findtext("date")
            ),

            "store_id": (
                elem.findtext("branch_code")
            ),

            "product_id": (
                elem.findtext("sku")
            ),

            "quantity": (
                elem.findtext("units")
            ),

            "unit_price": (
                elem.findtext("unit_value")
            ),

            "promotion_code": (
                elem.findtext("promo_code")
            ),

            "payment_method": (
                elem.findtext("payment")
            )
        })

    df = pd.DataFrame(records)

    return df[COMMON_COLUMNS]


# ============================================================
# EXTRACCIÓN DE TABLAS MAESTRAS
# ============================================================

def extract_reference_tables(data_dir):
    """
    Extrae las tablas maestras necesarias para
    las etapas posteriores de transformación e integración.
    """

    products = pd.read_csv(
        os.path.join(data_dir, "products.csv")
    )

    stores = pd.read_csv(
        os.path.join(data_dir, "stores.csv")
    )

    promotions = pd.read_csv(
        os.path.join(data_dir, "promotions.csv")
    )

    monthly_targets = pd.read_csv(
        os.path.join(data_dir, "monthly_targets.csv")
    )

    return (
        products,
        stores,
        promotions,
        monthly_targets
    )


# ============================================================
# EXTRACCIÓN DE TODAS LAS TRANSACCIONES
# ============================================================

def extract_all_transactions(data_dir):
    """
    Extrae las transacciones de Cali, Bogotá y Medellín
    y las concatena en un único DataFrame.

    IMPORTANTE:
    Aquí todavía NO se realiza limpieza ni transformación
    de negocio.
    """

    df_cali = extract_cali_csv(
        os.path.join(data_dir, "sales_cali.csv")
    )

    df_bogota = extract_bogota_json(
        os.path.join(data_dir, "sales_bogota.json")
    )

    df_medellin = extract_medellin_xml(
        os.path.join(data_dir, "sales_medellin.xml")
    )

    # Unificación de las tres fuentes
    raw_transactions = pd.concat(
        [
            df_cali,
            df_bogota,
            df_medellin
        ],
        ignore_index=True
    )

    return raw_transactions