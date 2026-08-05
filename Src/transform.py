import pandas as pd


# ============================================================
# PRODUCTOS
# ============================================================

def integrate_products(transactions, products):
    """
    Agrega la información de productos.
    """

    df = transactions.merge(
        products[
            [
                "product_id",
                "product_name",
                "category"
            ]
        ],
        on="product_id",
        how="left"
    )

    return df


# ============================================================
# TIENDAS
# ============================================================

def integrate_stores(df, stores):
    """
    Agrega la información de las tiendas.
    """

    df = df.merge(
        stores[
            [
                "store_id",
                "store_name",
                "city",
                "region"
            ]
        ],
        on="store_id",
        how="left"
    )

    return df


# ============================================================
# PROMOCIONES
# ============================================================

def integrate_promotions(df, promotions):
    """
    Agrega el porcentaje de descuento y
    el nombre de la campaña.
    """

    df = df.merge(
        promotions[
            [
                "promotion_code",
                "discount_pct",
                "campaign_name"
            ]
        ],
        on="promotion_code",
        how="left"
    )

    return df


# ============================================================
# VENTAS
# ============================================================

def calculate_sales(df):
    """
    Calcula gross_sales,
    discount_amount
    y net_sales.
    """

    # Promociones inexistentes
    df["discount_pct"] = (
        df["discount_pct"]
        .fillna(0)
    )

    df["gross_sales"] = (
        df["quantity"]
        * df["unit_price"]
    )

    df["discount_amount"] = (
        df["gross_sales"]
        * df["discount_pct"]
    )

    df["net_sales"] = (
        df["gross_sales"]
        - df["discount_amount"]
    )

    return df


# ============================================================
# FECHAS
# ============================================================

def create_date_columns(df):
    """
    Crea columnas derivadas de la fecha.
    """

    df["month"] = (
        df["sale_date"]
        .dt.month
    )

    df["week"] = (
        df["sale_date"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    df["day_name"] = (
        df["sale_date"]
        .dt.day_name()
    )

    return df


# ============================================================
# METAS
# ============================================================

def integrate_targets(df, monthly_targets):
    """
    Agrega la meta mensual correspondiente
    a cada tienda.
    """

    # Crear una columna con el mismo formato del archivo:
    # 2026-02, 2026-03, 2026-04
    df["month_target"] = df["sale_date"].dt.strftime("%Y-%m")

    df = df.merge(
        monthly_targets,
        left_on=["store_id", "month_target"],
        right_on=["store_id", "month"],
        how="left"
    )

    df.drop(columns=["month_target", "month_y"], inplace=True)

    df.rename(columns={"month_x": "month"}, inplace=True)

    return df


# ============================================================
# PIPELINE DE TRANSFORMACIÓN
# ============================================================

def transform_transactions(
    transactions,
    products,
    stores,
    promotions,
    monthly_targets
):
    """
    Ejecuta todas las transformaciones
    de la Actividad 6.
    """

    print("\n========== TRANSFORMACIÓN ==========\n")

    df = integrate_products(
        transactions,
        products
    )

    df = integrate_stores(
        df,
        stores
    )

    df = integrate_promotions(
        df,
        promotions
    )

    df = calculate_sales(df)

    df = create_date_columns(df)

    df = integrate_targets(
        df,
        monthly_targets
    )

    print("Transformación finalizada.\n")

    return df