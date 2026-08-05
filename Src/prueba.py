from queries import (
    query_total_sales,
    query_low_products,
    query_store_targets,
    query_promotions,
    query_time_trends,
    query_regions
)


def run_all_queries():

    print("\n")
    print("=" * 70)
    print("PRUEBA DE TODAS LAS CONSULTAS ANALÍTICAS")
    print("=" * 70)

    query_total_sales()

    print("\n" + "=" * 70)
    query_low_products()

    print("\n" + "=" * 70)
    query_store_targets()

    print("\n" + "=" * 70)
    query_promotions()

    print("\n" + "=" * 70)
    query_time_trends()

    print("\n" + "=" * 70)
    query_regions()

    print("\n" + "=" * 70)
    print("TODAS LAS CONSULTAS SE EJECUTARON CORRECTAMENTE")
    print("=" * 70)


if __name__ == "__main__":
    run_all_queries()