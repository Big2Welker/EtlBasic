# ETL Pipeline - Retail Analytics (Laboratorio 1B)

Sebastian Rojas Herrera, Juan David Bedoya

## Descripción general

Este proyecto implementa un pipeline ETL (Extract, Transform and Load) para integrar información de ventas provenientes de tres sucursales de una empresa de retail.

Las transacciones son extraídas desde archivos en diferentes formatos (CSV, JSON y XML), posteriormente se perfilan, limpian, transforman, validan y finalmente se cargan en un archivo CSV integrado y en una base de datos SQLite.

Finalmente se ejecutan consultas analíticas que permiten responder los requisitos de negocio definidos en el Laboratorio 1A.

---

# Arquitectura del sistema

```
                    +-------------------------+
                    |     Datos de entrada    |
                    +-------------------------+
                    | sales_cali.csv          |
                    | sales_bogota.json       |
                    | sales_medellin.xml      |
                    | products.csv            |
                    | stores.csv              |
                    | promotions.csv          |
                    | monthly_targets.csv     |
                    +------------+------------+
                                 |
                                 v
                      +--------------------+
                      |    EXTRACCIÓN      |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      |   PERFILAMIENTO    |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      | LIMPIEZA Y         |
                      | ARMONIZACIÓN       |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      | TRANSFORMACIÓN     |
                      | E INTEGRACIÓN      |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      |   VALIDACIÓN       |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      |      CARGA         |
                      +--------------------+
                           |           |
                           |           |
                           v           v
                 integrated_sales.csv
                      retail_analytics.db
                           |
                           v
                 Consultas Analíticas
```

---

# Requisitos de negocio implementados

El sistema permite responder los siguientes requisitos de negocio:

- Ingresos totales del negocio.
- Productos con menor rendimiento.
- Cumplimiento de metas por tienda.
- Impacto de campañas promocionales.
- Tendencias temporales de ventas.
- Comparación de ventas por región.

---

# Descripción del Pipeline ETL

## 1. Extracción

La etapa de extracción integra información proveniente de tres formatos distintos:

- CSV (Sucursal Cali)
- JSON (Sucursal Bogotá)
- XML (Sucursal Medellín)

Además, se cargan las tablas maestras:

- products.csv
- stores.csv
- promotions.csv
- monthly_targets.csv

Durante esta etapa únicamente se homologa el esquema de columnas; no se realizan modificaciones sobre los datos.

---

## 2. Perfilamiento

Antes de limpiar los datos se realizó un perfilamiento del conjunto de datos consolidado.

## Dimensiones

- Registros: **763**
- Columnas: **8**

## Columnas

- sale_line_id
- sale_date
- store_id
- product_id
- quantity
- unit_price
- promotion_code
- payment_method

## Tipos de datos encontrados

| Columna | Tipo original |
|----------|---------------|
| sale_line_id | str |
| sale_date | str |
| store_id | str |
| product_id | str |
| quantity | object |
| unit_price | object |
| promotion_code | str |
| payment_method | str |

## Valores faltantes

| Columna | Faltantes |
|----------|----------|
| promotion_code | 489 |

Las demás columnas no presentaron valores faltantes.

## Problemas encontrados

### IDs duplicados

Se encontraron **3 registros duplicados** en `sale_line_id`.

### Cantidades inválidas

Se detectaron **2 registros** con cantidad menor o igual a cero.

### Precios inválidos

Se encontraron **2 registros** con precio inválido.

Uno de ellos incluía el símbolo `$` y otro tenía un valor negativo.

### Fechas

Las ventas provenían de tres formatos distintos:

- YYYY-MM-DD
- DD/MM/YYYY
- MM-DD-YYYY

Por esta razón el perfilamiento inicial detectó numerosas fechas inválidas utilizando un único formato de lectura.

### Valores categóricos inconsistentes

Se detectaron diferencias de escritura como:

Store ID

- S02
- s02

Product ID

- P005
- " P005"

Payment Method

- Cash
- CASH
- card

Promotion Code

- NaN
- ""
- N/A

---
## 3. Limpieza y armonización

Las reglas aplicadas fueron definidas únicamente a partir de los resultados obtenidos durante el perfilamiento.

## Regla 1

Se estandarizaron los identificadores:

- sale_line_id
- store_id
- product_id

Aplicando:

- eliminación de espacios
- conversión a mayúsculas

Justificación:

Existían identificadores escritos como `s02` y `" P005"`.

---

## Regla 2

Se normalizaron los textos utilizando Title Case y eliminando espacios.

Justificación:

Existían valores como:

- CASH
- card
- Cash

---

## Regla 3

Las fechas fueron interpretadas utilizando el formato correspondiente para cada sucursal y convertidas a un único tipo `datetime`.

Justificación:

Cada ciudad utilizaba un formato diferente de fecha.

---

## Regla 4

Las columnas

- quantity
- unit_price

se convirtieron a valores numéricos.

Además se eliminó el símbolo `$` presente en algunos precios.

---

## Regla 5

Se eliminaron registros duplicados de `sale_line_id`, conservando únicamente la primera ocurrencia.

Justificación:

El perfilamiento encontró tres registros duplicados.

---

## Regla 6

Se eliminaron registros con:

- fechas inválidas
- quantity ≤ 0
- unit_price ≤ 0

Justificación:

Estos registros no cumplen las reglas de calidad del negocio.

---

## Regla 7

Los códigos de promoción faltantes fueron representados de forma consistente utilizando valores nulos (`NaN`).

Justificación:

Existían distintas representaciones:

- NaN
- ""
- N/A

---

## Resultado de la limpieza

Registros iniciales:

763

Registros finales:

756

Registros eliminados:

7

---

## 4. Transformación e integración

Las ventas son enriquecidas mediante la integración con las tablas maestras.

Se agregan los siguientes atributos:

- product_name
- category
- store_name
- city
- region
- discount_pct
- campaign_name
- sales_target

También se generan nuevas métricas:

- gross_sales
- discount_amount
- net_sales

Y nuevas variables temporales:

- month
- week
- day_name

---

## 5. Validación

Antes de realizar la carga se verifica que:

- sale_line_id sea único.
- Los identificadores obligatorios no sean nulos.
- Las fechas sean válidas.
- quantity, unit_price, gross_sales y net_sales sean positivos.
- Todos los productos existan en el maestro.
- Todas las tiendas existan en el maestro.
- net_sales sea igual a gross_sales menos discount_amount.

Si alguna validación falla, el pipeline se detiene y registra el error en el archivo de log.

---

## 6. Carga

Los datos procesados se almacenan en:

**CSV**

```
Data/processed/integrated_sales.csv
```

**SQLite**

```
Database/retail_analytics.db
```

Tabla creada:

```
sales_analytics
```

Todas las consultas analíticas leen directamente desde SQLite.

---

# Estructura del proyecto

```
ETL_Lab1B_Data_Only/

│
├── Data/
│   ├── raw/
│   │   ├── monthly_targets.csv
│   │   ├── products.csv
│   │   ├── promotions.csv
│   │   ├── sales_bogota.json
│   │   ├── sales_cali.csv
│   │   ├── sales_medellin.xml
│   │   └── stores.csv
│   │
│   └── processed/
│       └── integrated_sales.csv
│
├── Database/
│   └── retail_analytics.db
│
├── Logs/
│   └── pipeline.log
│
├── Src/
│   ├── clean.py
│   ├── extract.py
│   ├── load.py
│   ├── main.py
│   ├── profiling.py
│   ├── queries.py
│   ├── transform.py
│   ├── validate.py
│   ├── prueba.py
│   └── pruebas/
│
├── DATA_DICTIONARY.md
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Instrucciones de ejecución

## 1. Clonar el repositorio

```bash
git clone https://github.com/Big2Welker/EtlBasic.git
```

Entrar al proyecto

```bash
cd EtlBasic
```

---

## 2. Crear un entorno virtual

Windows

```bash
python -m venv .etl
```

Activar el entorno

```bash
.etl\Scripts\activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no existe el archivo requirements.txt:

```bash
pip install pandas
```

---

## 4. Ejecutar el pipeline

Los scripts fueron desarrollados para ejecutarse **desde la carpeta `Src`**, ya que utilizan rutas relativas hacia las carpetas `Data`, `Database` y `Logs`.

Ingresar a la carpeta:

```bash
cd Src
```

Ejecutar:

```bash
python main.py
```

---

Durante la ejecución el sistema realizará automáticamente:

1. Extracción.
2. Perfilamiento.
3. Limpieza y armonización.
4. Transformación.
5. Validación.
6. Carga.
7. Consultas analíticas.

---

Al finalizar se generarán automáticamente:

- `Data/processed/integrated_sales.csv`
- `Database/retail_analytics.db`
- `Logs/pipeline.log`

---

En la carpeta Src, hay unos .py de pruebas para ejecutar, ejecutarlos dentro de la carpeta Src, con el comando python prueba_nombre_de_la_prueba.py

# Tecnologías utilizadas

- Python 3
- Pandas
- SQLite3
- JSON
- XML
- CSV
- Logging

---

# Ejemplos de resultados analíticos

## Ingresos totales

```
Ventas Brutas:
$182.609.000

Ventas Netas:
$180.966.860
```

---

## Productos con menor rendimiento

```
Digital Scale
Notebook Pack
Keyboard Compact
Electric Shaver
Bluetooth Speaker
...
```

---

## Cumplimiento de metas

```
Bogotá Centro      93.69 %
Cali Norte        117.27 %
Medellín Poblado  109.13 %
```

---

## Tendencias temporales

```
Febrero
Marzo
Abril
```

---

## Ventas por región

```
Bogotá
Cali
Medellín
```

---

# Autores
Sebastian Rojas Herrera
Juan David Bedoya

Laboratorio 1B - Ingeniería de Datos

Proyecto académico desarrollado para la implementación de un pipeline ETL utilizando Python y SQLite.
