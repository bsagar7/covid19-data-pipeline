
# 🌐 COVID-19 Data Engineering Pipeline (2022)

This project demonstrates a complete data engineering workflow that extracts, stores, transforms, and visualizes global COVID-19 data for the year 2022. The pipeline leverages public APIs, cloud storage, and data warehouse tools to deliver a scalable, production-ready data system.

---

## 🔧 Tech Stack

- **Python** – API integration and data formatting
- **REST API** – [COVID-19 API](https://covid-api.com/api/reports/total)
- **AWS S3** – Raw data storage
- **Snowflake** – Data warehouse, transformation, and analytics
- **Snowpark (Python API)** – In-warehouse data transformations
- **SQL** – Data modeling, joins, and enrichment
- **Tableau** – Data visualization

---

## 🗂️ Project Architecture

```
         +-------------+        +--------------+        +---------------------+
         | COVID API   | -----> | Python Script | -----> | AWS S3 (Raw CSVs)   |
         +-------------+        +--------------+        +---------------------+
                                                            |
                                                            v
                                                   +----------------+
                                                   | Snowflake Stage |
                                                   +----------------+
                                                            |
                                                            v
                                          +----------------------------------+
                                          | Snowflake STAGING → RAW → CURATED|
                                          +----------------------------------+
                                                            |
                                                            v
                                          +----------------------------+
                                          | Tableau Dashboard          |
                                          +----------------------------+
```

---

## 🧪 Features

- ✅ **Automated Data Extraction** from COVID-19 API for each country and each month of 2022.
- ✅ **Data Storage in S3** as monthly `.csv` files using Python.
- ✅ **Ingestion into Snowflake** via external stage and `COPY INTO` statements.
- ✅ **Data Enrichment** using ISO country code mappings.
- ✅ **Snowpark Transformations** for schema cleaning and final table generation.
- ✅ **Interactive Dashboards** showing confirmed cases, deaths, active cases, and fatality rates by country.

---

## 📁 Folder Structure

```bash
.
├── scripts/
│   └── covid_api.py          # Extracts monthly country-level COVID data to AWS S3
│
├── snowflake/
│   ├── s3_snowflake.sql           # Table DDLs: STAGING, RAW, CURATED
│   ├── staging_raw.py          # Snowpark script to load and transform data
│   └── transformed.sql          # Enrich CURATED data with country names
│
├── dashboards/
│   └── Tableau_Dashboard.png      
│
└── README.md
```

---

## 🚀 How to Run

1. Clone the repo and set up a virtual environment.
2. Run the API extraction script:
   ```bash
   python3 scripts/covid_api.py
   ```
3. Load data into Snowflake using:
   - `snowflake/s3_snowflake.sql`
   - `snowflake/staging_raw.py`
   - `snowflake/transformed.sql`
4. Connect Tableau to your CURATED table.



## 📌 Learning Outcomes

- Hands-on experience with real-world data engineering tools.
- Working knowledge of API-based ingestion, staging architecture, and Snowflake pipeline design.
- Practical use of Snowpark for scalable data transformation.
- Enhanced data storytelling via dashboards and KPI tracking.

---

## 🧠 Future Improvements

- Schedule automated daily loads via Airflow or AWS Lambda.
- Add unit tests and logging to Python scripts.
- Include historical data at region or state level.


## 🙌 Acknowledgments

Thanks to [covid-api.com](https://covid-api.com) for providing free COVID-19 data.
