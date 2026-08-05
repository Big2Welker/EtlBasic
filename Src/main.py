import os
import logging

from extract import (
    extract_all_transactions,
    extract_reference_tables
)

from profiling import profile_transactions
from clean import clean_transactions
from transform import transform_transactions
from validate import validate_transactions
from load import load_data

# Ejecuta todas las consultas analíticas
from queries import menu


# ============================================================
# CONFIGURACIÓN DEL LOG
# ============================================================

os.makedirs("../Logs", exist_ok=True)

logging.basicConfig(
    filename="../Logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ============================================================
# MAIN
# ============================================================

def main():

    try:

        print("\n" + "=" * 60)
        print("PIPELINE ETL - LABORATORIO 1B")
        print("=" * 60)

        logging.info("Inicio del pipeline.")

        # ====================================================
        # 1. EXTRACCIÓN
        # ====================================================

        print("\n[1/7] Extracción")

        transactions = extract_all_transactions("../data/raw")

        products, stores, promotions, monthly_targets = \
            extract_reference_tables("../data/raw")

        print(f"✓ Registros extraídos: {len(transactions)}")

        logging.info(
            f"Extracción completada ({len(transactions)} registros)"
        )

        # ====================================================
        # 2. PERFILAMIENTO
        # ====================================================

        print("\n[2/7] Perfilamiento")

        profile_transactions(transactions)

        logging.info("Perfilamiento completado.")

        # ====================================================
        # 3. LIMPIEZA
        # ====================================================

        print("\n[3/7] Limpieza y armonización")

        transactions = clean_transactions(transactions)

        print(f"✓ Registros después de limpieza: {len(transactions)}")

        logging.info(
            f"Limpieza completada ({len(transactions)} registros)"
        )

        # ====================================================
        # 4. TRANSFORMACIÓN
        # ====================================================

        print("\n[4/7] Transformación e integración")

        transactions = transform_transactions(
            transactions,
            products,
            stores,
            promotions,
            monthly_targets
        )

        print(
            f"✓ Dataset transformado: {len(transactions)} registros"
        )

        logging.info("Transformación completada.")

        # ====================================================
        # 5. VALIDACIÓN
        # ====================================================

        print("\n[5/7] Validación")

        validate_transactions(transactions)

        logging.info("Validación completada.")

        # ====================================================
        # 6. CARGA
        # ====================================================

        print("\n[6/7] Carga")

        load_data(transactions)

        logging.info("Carga completada.")

        # ====================================================
        # 7. CONSULTAS ANALÍTICAS
        # ====================================================

        print("\n[7/7] Consultas analíticas")

        menu()

        logging.info("Consultas analíticas ejecutadas.")

        # ====================================================

        print("\n" + "=" * 60)
        print("PIPELINE FINALIZADO CORRECTAMENTE")
        print("=" * 60)

        logging.info("Pipeline finalizado correctamente.")

    except Exception as e:

        logging.exception("Error durante la ejecución del pipeline.")

        print("\n" + "=" * 60)
        print("ERROR EN EL PIPELINE")
        print("=" * 60)
        print(e)

        raise


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()