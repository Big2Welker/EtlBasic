import os
import sqlite3


# ============================================================
# GUARDAR CSV
# ============================================================

def save_csv(df, output_dir):
    """
    Guarda el dataset integrado en formato CSV.
    """

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        "integrated_sales.csv"
    )

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )

    print(f"✓ CSV guardado en: {output_file}")


# ============================================================
# CARGAR SQLITE
# ============================================================

def load_sqlite(df, db_path):
    """
    Carga el dataset en una base de datos SQLite.
    Si la base de datos no existe, SQLite la crea automáticamente.
    """

    # Crear la carpeta donde se almacenará la base de datos
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Conectar a SQLite
    conn = sqlite3.connect(db_path)

    # Crear/Reemplazar la tabla
    df.to_sql(
        "sales_analytics",
        conn,
        if_exists="replace",
        index=False
    )

    # Cerrar conexión
    conn.close()

    print(f"✓ Base de datos creada en: {db_path}")


# ============================================================
# PIPELINE DE CARGA
# ============================================================

def load_data(df):

    print("\n========== CARGA ==========\n")

    # Guardar CSV procesado
    save_csv(
        df,
        "../data/processed"
    )

    # Guardar base de datos SQLite
    load_sqlite(
        df,
        "../Database/retail_analytics.db"
    )

    print("\nCarga finalizada correctamente.\n")