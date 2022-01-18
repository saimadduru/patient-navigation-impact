"""
Loads the synthetic cohort CSV into a SQLite database.
Mirrors how a real analyst loads claims data into Snowflake/BigQuery.
"""

import sqlite3
import pandas as pd
import os

DB_PATH = "data/claims.db"

df = pd.read_csv("data/synthetic_cohort.csv")

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS patient_encounters;
DROP TABLE IF EXISTS diagnoses;
DROP TABLE IF EXISTS utilization;
DROP TABLE IF EXISTS navigation_enrollment;

-- Core patient + index admission table (mirrors claims enrollment file)
CREATE TABLE patient_encounters (
    patient_id      TEXT PRIMARY KEY,
    age             INTEGER,
    female          INTEGER,
    dual_eligible   INTEGER,
    rural           INTEGER,
    index_los       INTEGER
);

-- Diagnosis / comorbidity table (mirrors ICD-10 claims data)
CREATE TABLE diagnoses (
    patient_id  TEXT,
    cci         INTEGER,
    chf         INTEGER,
    copd        INTEGER,
    diabetes    INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patient_encounters(patient_id)
);

-- Utilization outcomes table (mirrors claims utilization file)
CREATE TABLE utilization (
    patient_id          TEXT,
    prior_admits_12m    INTEGER,
    readmit_30d         INTEGER,
    er_visits_90d       INTEGER,
    total_cost_180d     INTEGER,
    days_to_readmit     INTEGER,
    event_observed      INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patient_encounters(patient_id)
);

-- Navigation enrollment table (mirrors program enrollment registry)
CREATE TABLE navigation_enrollment (
    patient_id  TEXT,
    navigated   INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patient_encounters(patient_id)
);
""")

df[["patient_id","age","female","dual_eligible","rural","index_los"]]\
    .to_sql("patient_encounters", conn, if_exists="append", index=False)

df[["patient_id","cci","chf","copd","diabetes"]]\
    .to_sql("diagnoses", conn, if_exists="append", index=False)

df[["patient_id","prior_admits_12m","readmit_30d","er_visits_90d",
    "total_cost_180d","days_to_readmit","event_observed"]]\
    .to_sql("utilization", conn, if_exists="append", index=False)

df[["patient_id","navigated"]]\
    .to_sql("navigation_enrollment", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print(f"Database created: {DB_PATH}")
print(f"Tables: patient_encounters, diagnoses, utilization, navigation_enrollment")
print(f"Rows loaded: {len(df):,}")
