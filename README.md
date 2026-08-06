# ETL Pipeline - Retail Analytics (Lab 1B)

Sebastian Rojas Herrera, Juan David Bedoya

---

## Overview

This project implements an ETL (Extract, Transform, and Load) pipeline to integrate sales information from three branches of a retail company.

Transactions are extracted from files in different formats (CSV, JSON, and XML). The data is then profiled, cleaned, transformed, validated, and finally loaded into an integrated CSV file and a SQLite database.

Finally, analytical queries are executed to answer the business requirements defined in Laboratory 1A.

---

# System Architecture

```text
                    +-------------------------+
                    |      Input Data         |
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
                      |     EXTRACTION     |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      |     PROFILING      |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      | CLEANING &         |
                      | HARMONIZATION      |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      | TRANSFORMATION &   |
                      | INTEGRATION        |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      |    VALIDATION      |
                      +--------------------+
                                 |
                                 v
                      +--------------------+
                      |      LOADING       |
                      +--------------------+
                           |           |
                           |           |
                           v           v
                integrated_sales.csv
                   retail_analytics.db
                           |
                           v
                  Analytical Queries
```

---

# Implemented Business Requirements

The system answers the following business questions:

- Total business revenue
- Lowest-performing products
- Store target achievement
- Promotional campaign impact
- Sales trends over time
- Regional sales comparison

---

# ETL Pipeline Description

## 1. Extraction

The extraction stage integrates information from three different file formats:

- CSV (Cali Branch)
- JSON (Bogotá Branch)
- XML (Medellín Branch)

It also loads the following master tables:

- products.csv
- stores.csv
- promotions.csv
- monthly_targets.csv

During this stage, only the column schema is standardized. No modifications are made to the data itself.

---

## 2. Profiling

Before cleaning, a data profiling process was performed on the consolidated dataset.

### Dataset Dimensions

- Records: **763**
- Columns: **8**

### Columns

- sale_line_id
- sale_date
- store_id
- product_id
- quantity
- unit_price
- promotion_code
- payment_method

### Original Data Types

| Column | Original Type |
|----------|--------------|
| sale_line_id | str |
| sale_date | str |
| store_id | str |
| product_id | str |
| quantity | object |
| unit_price | object |
| promotion_code | str |
| payment_method | str |

### Missing Values

| Column | Missing Values |
|----------|---------------|
| promotion_code | 489 |

All other columns contained no missing values.

### Identified Issues

#### Duplicate IDs

Three duplicate `sale_line_id` records were found.

#### Invalid Quantities

Two records had quantities less than or equal to zero.

#### Invalid Prices

Two records contained invalid prices.

One included the `$` symbol, while another contained a negative value.

#### Dates

Sales data came in three different formats:

- YYYY-MM-DD
- DD/MM/YYYY
- MM-DD-YYYY

As a result, the initial profiling detected multiple invalid dates when using a single parsing format.

#### Inconsistent Categorical Values

Examples:

**Store ID**

- S02
- s02

**Product ID**

- P005
- " P005"

**Payment Method**

- Cash
- CASH
- card

**Promotion Code**

- NaN
- ""
- N/A

---

## 3. Cleaning and Harmonization

The cleaning rules were defined exclusively based on the profiling results.

### Rule 1

Standardize identifiers:

- sale_line_id
- store_id
- product_id

Actions:

- Remove leading/trailing spaces
- Convert to uppercase

Reason:

Identifiers such as `s02` and `" P005"` were found.

---

### Rule 2

Normalize text values using Title Case and remove extra spaces.

Reason:

Values such as:

- CASH
- card
- Cash

---

### Rule 3

Parse dates according to each branch's original format and convert them into a unified `datetime` type.

Reason:

Each city used a different date format.

---

### Rule 4

Convert:

- quantity
- unit_price

to numeric values.

Additionally, remove the `$` symbol from price values.

---

### Rule 5

Remove duplicate `sale_line_id` records, keeping only the first occurrence.

Reason:

Three duplicate IDs were detected during profiling.

---

### Rule 6

Remove records containing:

- Invalid dates
- quantity ≤ 0
- unit_price ≤ 0

Reason:

These records violate business data quality rules.

---

### Rule 7

Represent missing promotion codes consistently using `NaN`.

Reason:

Different missing-value representations existed:

- NaN
- ""
- N/A

---

### Cleaning Results

Initial records:

763

Final records:

756

Removed records:

7

---

## 4. Transformation and Integration

Sales records are enriched by joining them with the master tables.

The following attributes are added:

- product_name
- category
- store_name
- city
- region
- discount_pct
- campaign_name
- sales_target

Additional metrics are calculated:

- gross_sales
- discount_amount
- net_sales

Additional time-based variables:

- month
- week
- day_name

---

## 5. Validation

Before loading, the following checks are performed:

- sale_line_id is unique
- Required identifiers are not null
- Dates are valid
- quantity, unit_price, gross_sales, and net_sales are positive
- Products exist in the master table
- Stores exist in the master table
- net_sales equals gross_sales minus discount_amount

If any validation fails, the pipeline stops and logs the error.

---

## 6. Loading

Processed data is stored in:

### CSV

```
Data/processed/integrated_sales.csv
```

### SQLite

```
Database/retail_analytics.db
```

Created table:

```
sales_analytics
```

All analytical queries read directly from SQLite.

---

# Project Structure

```text
ETL_Lab1B_Data_Only/

├── Data/
│   ├── raw/
│   └── processed/
├── Database/
├── Logs/
├── Src/
├── DATA_DICTIONARY.md
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Execution Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/Big2Welker/EtlBasic.git
```

Enter the project folder:

```bash
cd EtlBasic
```

---

## 2. Create a Virtual Environment

Windows

```bash
python -m venv .etl
```

Activate it:

```bash
.etl\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist:

```bash
pip install pandas
```

---

## 4. Run the Pipeline

The scripts were designed to be executed from the **Src** directory because they use relative paths to the `Data`, `Database`, and `Logs` folders.

```bash
cd Src
```

Run:

```bash
python main.py
```

---

During execution, the pipeline automatically performs:

1. Extraction
2. Profiling
3. Cleaning and Harmonization
4. Transformation
5. Validation
6. Loading
7. Analytical Queries

---

Generated outputs:

- `Data/processed/integrated_sales.csv`
- `Database/retail_analytics.db`
- `Logs/pipeline.log`

---

Testing scripts are located inside the **Src** folder.

Run them using:

```bash
python test_script_name.py
```

---

# Technologies Used

- Python 3
- Pandas
- SQLite3
- JSON
- XML
- CSV
- Logging

---

# Sample Analytical Results

## Total Revenue

```text
Gross Sales:
$182,609,000

Net Sales:
$180,966,860
```

---

## Lowest-Performing Products

```text
Digital Scale
Notebook Pack
Keyboard Compact
Electric Shaver
Bluetooth Speaker
...
```

---

## Target Achievement

```text
Bogotá Centro       93.69%
Cali Norte         117.27%
Medellín Poblado   109.13%
```

---

## Sales Trends

```text
February
March
April
```

---

## Sales by Region

```text
Bogotá
Cali
Medellín
```

---

# Reflection Questions

## 1. How did the Laboratory 1A requirements influence the pipeline design?

The Laboratory 1A requirements served as the foundation for designing the ETL pipeline. They defined the business questions to answer, which determined the required data sources, transformations, and analytical queries. Each pipeline stage was designed to produce a dataset capable of supporting business decision-making.

---

## 2. What is the difference between profiling, cleaning, transformation, and validation?

- **Profiling:** Analyzes data quality before any modifications.
- **Cleaning:** Corrects issues identified during profiling.
- **Transformation:** Integrates data and generates new business attributes and metrics.
- **Validation:** Ensures the final dataset complies with business quality rules before loading.

---

## 3. Why was it necessary to design the system in blocks before coding?

Designing the pipeline in modular blocks separated responsibilities, making development, testing, and maintenance easier. Each module performs a single task, improving organization, reusability, and scalability.

---

## 4. Which module would be most affected if a branch changed its file format?

The **Extraction** module would be the most affected because it is responsible for reading and standardizing input files. The remaining ETL stages could remain unchanged.

---

## 5. Did the team build an ETL pipeline or a business solution?

Technically, the project implements an ETL pipeline. However, its ultimate goal is to solve a business problem by providing reliable analytical information for decision-making. The ETL process is the mechanism, while the complete system delivers meaningful business insights.

---

# Authors

Sebastian Rojas Herrera

Juan David Bedoya

**Data Engineering Laboratory 1B**

Academic project developed to implement an ETL pipeline using Python and SQLite.
