
-- TOTAL PRODUCTS
SELECT COUNT(*) AS total_products FROM retail.fact_sales;

-- AVG RATING
SELECT ROUND(AVG(rating),2) AS avg_rating FROM retail.fact_sales;

-- AVG DISCOUNT
SELECT ROUND(AVG(discount_percentage),2) AS avg_discount FROM retail.fact_sales;

-- TOTAL SAVINGS
SELECT ROUND(SUM(savings),2) AS total_savings FROM retail.fact_sales;

-- CATEGORY ANALYSIS
SELECT 
    category,
    COUNT(*) AS total_products,
    ROUND(AVG(discount_percentage),2) AS avg_discount,
    ROUND(AVG(rating),2) AS avg_rating
FROM retail.fact_sales
GROUP BY category
ORDER BY total_products DESC;

-- TOP RATED
SELECT 
    product_name,
    rating,
    rating_count
FROM retail.fact_sales
WHERE rating >= 4.5
ORDER BY rating DESC, rating_count DESC
LIMIT 10;

-- HIGHEST DISCOUNT
SELECT 
    product_name,
    actual_price,
    discounted_price,
    discount_percentage
FROM retail.fact_sales
ORDER BY discount_percentage DESC
LIMIT 10;

-- PRICE BUCKET
SELECT 
    CASE 
        WHEN discounted_price < 500 THEN 'Low'
        WHEN discounted_price BETWEEN 500 AND 2000 THEN 'Medium'
        ELSE 'High'
    END AS price_bucket,
    ROUND(AVG(rating),2) AS avg_rating,
    COUNT(*) AS total_products
FROM retail.fact_sales
GROUP BY price_bucket
ORDER BY price_bucket;

-- KPI FLAG
SELECT 
    product_name,
    rating,
    discount_percentage,
    CASE 
        WHEN rating >= 4.2 AND discount_percentage >= 40 THEN 'High Performer'
        ELSE 'Normal'
    END AS performance_flag
FROM retail.fact_sales;

-- TREND
SELECT 
    DATE(processed_at) AS load_date,
    COUNT(*) AS records_loaded
FROM retail.fact_sales
GROUP BY load_date
ORDER BY load_date;

-- SLICER DATA
SELECT 
    category,
    product_name,
    discounted_price,
    rating,
    rating_count,
    discount_percentage,
    savings
FROM retail.fact_sales;
