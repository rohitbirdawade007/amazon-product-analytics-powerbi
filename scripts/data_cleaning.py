import pandas as pd

df = pd.read_csv('data/raw_data.csv', encoding='latin1')

df = df.drop_duplicates()

df = df.replace(['', ' ', 'NA', 'N/A', 'null', 'None'], pd.NA)

df['discounted_price'] = df['discounted_price'].replace('[₹,]', '', regex=True)
df['actual_price'] = df['actual_price'].replace('[₹,]', '', regex=True)

df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')

df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating_count'] = df['rating_count'].replace('[,]', '', regex=True)
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

df['discounted_price'] = df['discounted_price'].fillna(df['discounted_price'].median())
df['actual_price'] = df['actual_price'].fillna(df['actual_price'].median())
df['rating'] = df['rating'].fillna(df['rating'].median())
df['rating_count'] = df['rating_count'].fillna(0)

df['savings'] = df['actual_price'] - df['discounted_price']

cat_split = df['category'].fillna('Unknown').str.split('|', expand=True)
for i in range(cat_split.shape[1]):
    df[f'category_L{i+1}'] = cat_split[i]

df['brand'] = df['product_name'].fillna('Unknown').str.split(' ').str[0]

df['product_type'] = df['category_L1']

df['length'] = df['product_name'].fillna('').str.len()

df['color'] = df['product_name'].str.extract(r'(Black|White|Red|Blue|Green|Grey|Silver|Gold)', expand=False)
df['color'] = df['color'].fillna('Other')

df['features'] = df['about_product'].fillna('').str[:100]

df['product_name_clean'] = df['product_name'].fillna('').str.lower().str.replace('[^a-z0-9 ]', '', regex=True)

df['processed_at'] = pd.Timestamp.now()

df.to_csv('data/cleaned_data.csv', index=False)