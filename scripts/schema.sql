
-- =========================
-- SCHEMA
-- =========================
CREATE SCHEMA IF NOT EXISTS retail;

-- =========================
-- FLAT TABLE (FOR DIRECT POWER BI)
-- =========================
CREATE TABLE IF NOT EXISTS retail.fact_sales (
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

-- =========================
-- INDEXES (FLAT TABLE)
-- =========================
CREATE INDEX IF NOT EXISTS idx_category ON retail.fact_sales(category);
CREATE INDEX IF NOT EXISTS idx_rating ON retail.fact_sales(rating);
CREATE INDEX IF NOT EXISTS idx_price ON retail.fact_sales(discounted_price);
CREATE INDEX IF NOT EXISTS idx_processed_at ON retail.fact_sales(processed_at);

-- =========================
-- STAR SCHEMA
-- =========================

CREATE TABLE IF NOT EXISTS retail.dim_category (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS retail.dim_product (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category_id INT REFERENCES retail.dim_category(category_id)
);

CREATE TABLE IF NOT EXISTS retail.fact_sales_star (
    id SERIAL PRIMARY KEY,
    product_id TEXT REFERENCES retail.dim_product(product_id),
    discounted_price NUMERIC,
    actual_price NUMERIC,
    discount_percentage NUMERIC,
    rating NUMERIC,
    rating_count NUMERIC,
    savings NUMERIC,
    processed_at TIMESTAMP
);

-- =========================
-- INDEXES (STAR)
-- =========================
CREATE INDEX IF NOT EXISTS idx_star_product ON retail.fact_sales_star(product_id);
CREATE INDEX IF NOT EXISTS idx_star_rating ON retail.fact_sales_star(rating);
CREATE INDEX IF NOT EXISTS idx_star_price ON retail.fact_sales_star(discounted_price);
CREATE INDEX IF NOT EXISTS idx_star_time ON retail.fact_sales_star(processed_at);

-- =========================
-- STAGING TABLE
-- =========================
CREATE TABLE IF NOT EXISTS retail.staging_sales (
    product_id TEXT,
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

-- =========================
-- LOAD DIM_CATEGORY
-- =========================
INSERT INTO retail.dim_category (category_name)
SELECT DISTINCT category FROM retail.staging_sales
ON CONFLICT (category_name) DO NOTHING;

-- =========================
-- LOAD DIM_PRODUCT
-- =========================
INSERT INTO retail.dim_product (product_id, product_name, category_id)
SELECT 
    s.product_id,
    s.product_name,
    c.category_id
FROM retail.staging_sales s
JOIN retail.dim_category c 
ON s.category = c.category_name
ON CONFLICT (product_id) DO NOTHING;

-- =========================
-- LOAD STAR FACT
-- =========================
INSERT INTO retail.fact_sales_star (
    product_id,
    discounted_price,
    actual_price,
    discount_percentage,
    rating,
    rating_count,
    savings,
    processed_at
)
SELECT 
    product_id,
    discounted_price,
    actual_price,
    discount_percentage,
    rating,
    rating_count,
    savings,
    processed_at
FROM retail.staging_sales;
