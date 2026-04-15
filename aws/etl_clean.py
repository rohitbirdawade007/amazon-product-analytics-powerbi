import pandas as pd
import os
from datetime import datetime

INPUT = "data/amazon.csv"
OUTPUT = "data/processed/retail_clean.csv"

def main():
    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_csv(INPUT, encoding="latin1")

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    df = df.drop_duplicates()

    df = df.replace(['', ' ', 'NA', 'N/A', 'null', 'None', '|', '—'], pd.NA)

    def to_num(s):
        return pd.to_numeric(
            s.astype(str)
             .str.replace("₹", "", regex=False)
             .str.replace(",", "", regex=False)
             .str.replace("%", "", regex=False),
            errors="coerce"
        )

    for c in ["discounted_price", "actual_price", "discount_percentage", "rating", "rating_count"]:
        if c in df.columns:
            df[c] = to_num(df[c])

    df["discounted_price"] = df["discounted_price"].fillna(df["discounted_price"].median())
    df["actual_price"] = df["actual_price"].fillna(df["actual_price"].median())
    df["rating"] = df["rating"].fillna(df["rating"].median())
    df["rating_count"] = df["rating_count"].fillna(0)

    df = df[df["actual_price"] >= df["discounted_price"]]

    df["savings"] = df["actual_price"] - df["discounted_price"]

    df["discount_percentage"] = ((df["savings"] / df["actual_price"]) * 100).round(2)

    cat = df["category"].fillna("Unknown").str.split("|", expand=True)
    for i in range(cat.shape[1]):
        df[f"category_L{i+1}"] = cat[i]

    df["brand"] = df["product_name"].fillna("Unknown").str.split(" ").str[0]

    df["product_name_clean"] = df["product_name"].fillna("").str.lower().str.replace("[^a-z0-9 ]", "", regex=True)

    df["color"] = df["product_name"].str.extract(r'(Black|White|Red|Blue|Green|Grey|Silver|Gold)', expand=False).fillna("Other")

    df["processed_at"] = datetime.now()

    df.to_csv(OUTPUT, index=False)

    print(f"Saved → {OUTPUT}, rows={len(df)}")

if __name__ == "__main__":
    main()