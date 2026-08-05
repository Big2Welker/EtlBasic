import sqlite3
import pandas as pd

DB_PATH = "../Database/retail_analytics.db"


# ============================================================
# CONEXIÓN
# ============================================================

def execute_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# ============================================================
# FORMATO DE DINERO
# ============================================================

def money(value):
    return f"${value:,.0f}".replace(",", ".")


# ============================================================
# 1. INGRESOS TOTALES
# ============================================================

def query_total_sales():

    print("\n======================================================")
    print(" REQUISITO 1 - INGRESOS TOTALES DEL NEGOCIO")
    print("======================================================")

    query = """
    SELECT
        SUM(gross_sales) AS gross_sales,
        SUM(net_sales) AS net_sales
    FROM sales_analytics;
    """

    df = execute_query(query)

    gross = df.loc[0, "gross_sales"]
    net = df.loc[0, "net_sales"]

    print(f"\nVentas Brutas : {money(gross)}")
    print(f"Ventas Netas  : {money(net)}")

    print("""
Interpretación:
Permite conocer el volumen total de ventas del negocio y
evaluar el desempeño financiero general.
""")


# ============================================================
# 2. PRODUCTOS CON MENOR RENDIMIENTO
# ============================================================

def query_low_products():

    print("\n======================================================")
    print(" REQUISITO 2 - PRODUCTOS CON MENOR RENDIMIENTO")
    print("======================================================")

    query = """
    SELECT
        product_name,
        category,
        SUM(net_sales) AS total_sales
    FROM sales_analytics
    GROUP BY product_name, category
    ORDER BY total_sales ASC
    LIMIT 10;
    """

    df = execute_query(query)

    for _, row in df.iterrows():
        print(f"{row['product_name']:<25} {money(row['total_sales'])}")

    print("""
Interpretación:
Estos productos presentan el menor volumen de ventas y pueden
requerir promociones o estrategias comerciales.
""")


# ============================================================
# 3. CUMPLIMIENTO DE METAS
# ============================================================

def query_store_targets():

    print("\n======================================================")
    print(" REQUISITO 3 - CUMPLIMIENTO DE METAS")
    print("======================================================")

    query = """
    SELECT
        month,
        store_name,
        sales_target,
        SUM(net_sales) AS total_sales,
        ROUND(
            SUM(net_sales)*100.0/sales_target,
            2
        ) AS target_percentage
    FROM sales_analytics
    GROUP BY
        month,
        store_name,
        sales_target
    ORDER BY
        month,
        store_name;
    """

    df = execute_query(query)

    for _, row in df.iterrows():

        print(f"""
Mes: {row['month']}
Tienda: {row['store_name']}
Meta: {money(row['sales_target'])}
Ventas: {money(row['total_sales'])}
Cumplimiento: {row['target_percentage']} %
----------------------------------------------------
""")

    print("""
Interpretación:
Permite evaluar si cada tienda alcanzó la meta de ventas
establecida para cada mes.
""")


# ============================================================
# 4. IMPACTO DE PROMOCIONES
# ============================================================

def query_promotions():

    print("\n======================================================")
    print(" REQUISITO 4 - IMPACTO DE PROMOCIONES")
    print("======================================================")

    query = """
    SELECT
        campaign_name,
        COUNT(*) AS transactions,
        SUM(discount_amount) AS total_discount,
        SUM(net_sales) AS total_sales
    FROM sales_analytics
    WHERE campaign_name IS NOT NULL
    GROUP BY campaign_name
    ORDER BY total_sales DESC;
    """

    df = execute_query(query)

    for _, row in df.iterrows():

        print(f"""
Campaña: {row['campaign_name']}
Transacciones: {row['transactions']}
Descuento otorgado: {money(row['total_discount'])}
Ventas generadas: {money(row['total_sales'])}
----------------------------------------------------
""")

    print("""
Interpretación:
Permite analizar el impacto económico de cada campaña
promocional sobre las ventas.
""")


# ============================================================
# 5. TENDENCIAS TEMPORALES
# ============================================================

def query_time_trends():

    print("\n======================================================")
    print(" REQUISITO 5 - TENDENCIAS TEMPORALES")
    print("======================================================")

    query = """
    SELECT
        month,
        SUM(net_sales) AS total_sales
    FROM sales_analytics
    GROUP BY month
    ORDER BY month;
    """

    df = execute_query(query)

    meses = {
        2: "Febrero",
        3: "Marzo",
        4: "Abril"
    }

    for _, row in df.iterrows():

        print(
            f"{meses.get(row['month'], row['month'])}: "
            f"{money(row['total_sales'])}"
        )

    print("""
Interpretación:
Resume el comportamiento de las ventas a lo largo del tiempo,
permitiendo identificar tendencias mensuales.
""")


# ============================================================
# 6. VENTAS POR REGIÓN
# ============================================================

def query_regions():

    print("\n======================================================")
    print(" REQUISITO 6 - VENTAS POR REGIÓN")
    print("======================================================")

    query = """
    SELECT
        city,
        region,
        SUM(net_sales) AS total_sales
    FROM sales_analytics
    GROUP BY city, region
    ORDER BY total_sales DESC;
    """

    df = execute_query(query)

    for _, row in df.iterrows():

        print(
            f"{row['city']} ({row['region']})"
            f" -> {money(row['total_sales'])}"
        )

    print("""
Interpretación:
Permite comparar el desempeño comercial entre ciudades y
regiones para apoyar la toma de decisiones.
""")


# ============================================================
# MENÚ
# ============================================================

def menu():

    while True:

        print("""
======================================================
        CONSULTAS ANALÍTICAS - LABORATORIO 1B
======================================================

1. Ingresos totales del negocio
2. Productos con menor rendimiento
3. Cumplimiento de metas por tienda
4. Impacto de promociones
5. Tendencias temporales
6. Ventas por región
0. Salir
""")

        option = input("Seleccione una opción: ")

        if option == "1":
            query_total_sales()

        elif option == "2":
            query_low_products()

        elif option == "3":
            query_store_targets()

        elif option == "4":
            query_promotions()

        elif option == "5":
            query_time_trends()

        elif option == "6":
            query_regions()

        elif option == "0":
            print("\nGracias por usar el sistema.\n")
            break

        else:
            print("\nOpción inválida.\n")


if __name__ == "__main__":
    menu()