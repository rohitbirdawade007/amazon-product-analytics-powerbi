import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os

HOST = os.getenv("DB_HOST")
DB   = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PWD  = os.getenv("DB_PASS")
PORT = 5432

CSV_PATH = "data/processed/retail_clean.csv"

df = pd.read_csv(CSV_PATH)

cols = [
    "product_id","product_name","category",
    "discounted_price","actual_price","discount_percentage",
    "rating","rating_count","savings","processed_at"
]
df = df[cols].copy()

df = df.drop_duplicates(subset=["product_id"])

df = df.fillna({
    "product_id": "",
    "product_name": "",
    "category": "",
    "discounted_price": 0,
    "actual_price": 0,
    "discount_percentage": 0,
    "rating": 0,
    "rating_count": 0,
    "savings": 0,
})

num_cols = ["discounted_price","actual_price","discount_percentage","rating","rating_count","savings"]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

df["processed_at"] = pd.to_datetime(df["processed_at"], errors="coerce")

conn = psycopg2.connect(
    host=HOST, database=DB, user=USER, password=PWD, port=PORT
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS fact_sales (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    discounted_price NUMERIC,
    actual_price NUMERIC,
    discount_percentage NUMERIC,
    rating NUMERIC,
    rating_count NUMERIC,
    savings NUMERIC,
    processed_at TIMESTAMP
);
""")
conn.commit()

records = list(df.itertuples(index=False, name=None))

insert_sql = """
INSERT INTO fact_sales (
    product_id, product_name, category,
    discounted_price, actual_price, discount_percentage,
    rating, rating_count, savings, processed_at
)
VALUES %s
ON CONFLICT (product_id) DO UPDATE SET
    product_name = EXCLUDED.product_name,
    category = EXCLUDED.category,
    discounted_price = EXCLUDED.discounted_price,
    actual_price = EXCLUDED.actual_price,
    discount_percentage = EXCLUDED.discount_percentage,
    rating = EXCLUDED.rating,
    rating_count = EXCLUDED.rating_count,
    savings = EXCLUDED.savings,
    processed_at = EXCLUDED.processed_at;
"""

execute_values(cur, insert_sql, records, page_size=1000)
conn.commit()

cur.close()
conn.close()

print(f"Loaded {len(records)} rows into fact_sales")