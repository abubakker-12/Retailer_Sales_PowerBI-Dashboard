import pandas as pd
from pathlib import Path

print("Python environment ready")

# ---------------------------------------------------------
# 1. FILE LOCATIONS
# ---------------------------------------------------------

BASE_DIR = Path(r"C:\Users\HUAWEI 1\OneDrive\Documents\Global+Electronics+Retailer")
OUTPUT_DIR = BASE_DIR / "cleaned_data"

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# 2. LOAD RAW DATA
# ---------------------------------------------------------

sales = pd.read_csv(BASE_DIR / "Sales.csv")
products = pd.read_csv(BASE_DIR / "Products.csv", encoding="cp1252")
customers = pd.read_csv(BASE_DIR / "Customers.csv", encoding="cp1252")
stores = pd.read_csv(BASE_DIR / "Stores.csv", encoding="cp1252")
exchange_rates = pd.read_csv(BASE_DIR / "Exchange_Rates.csv")
data_dictionary = pd.read_csv(BASE_DIR / "Data_Dictionary.csv")

print("\nAll raw datasets loaded successfully.")


# ---------------------------------------------------------
# 3. SALES CLEANING
# ---------------------------------------------------------

# Convert dates
sales["Order Date"] = pd.to_datetime(
    sales["Order Date"],
    errors="coerce",
    dayfirst=False
)

sales["Delivery Date"] = pd.to_datetime(
    sales["Delivery Date"],
    errors="coerce",
    dayfirst=False
)

# Create sales channel
sales["Channel"] = sales["StoreKey"].apply(
    lambda x: "Online" if x == 0 else "In-Store"
)

# Remove exact duplicate rows
sales = sales.drop_duplicates()


# ---------------------------------------------------------
# 4. PRODUCT CLEANING
# ---------------------------------------------------------

# Clean product currency columns
for col in ["Unit Cost USD", "Unit Price USD"]:
    products[col] = (
        products[col]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    products[col] = pd.to_numeric(
        products[col],
        errors="coerce"
    )

# Remove exact duplicate rows
products = products.drop_duplicates()

# ---------------------------------------------------------
# 5. CUSTOMER CLEANING
# ---------------------------------------------------------

# Convert Birthday to date
customers["Birthday"] = pd.to_datetime(
    customers["Birthday"],
    errors="coerce"
)

# Remove exact duplicate rows
customers = customers.drop_duplicates()


# ---------------------------------------------------------
# 6. STORE CLEANING
# ---------------------------------------------------------

# Convert Open Date to date
stores["Open Date"] = pd.to_datetime(
    stores["Open Date"],
    errors="coerce"
)

# Keep StoreKey = 0 Square Meters as NULL
# because it represents Online sales.

stores = stores.drop_duplicates()


# ---------------------------------------------------------
# 7. EXCHANGE RATE CLEANING
# ---------------------------------------------------------

exchange_rates["Date"] = pd.to_datetime(
    exchange_rates["Date"],
    errors="coerce"
)

exchange_rates = exchange_rates.drop_duplicates()


# ---------------------------------------------------------
# 8. SAVE CLEANED DATA
# ---------------------------------------------------------

sales.to_csv(
    OUTPUT_DIR / "Sales_Cleaned.csv",
    index=False,
    encoding="utf-8"
)

products.to_csv(
    OUTPUT_DIR / "Products_Cleaned.csv",
    index=False,
    encoding="utf-8"
)

customers.to_csv(
    OUTPUT_DIR / "Customers_Cleaned.csv",
    index=False,
    encoding="utf-8"
)

stores.to_csv(
    OUTPUT_DIR / "Stores_Cleaned.csv",
    index=False,
    encoding="utf-8"
)

exchange_rates.to_csv(
    OUTPUT_DIR / "Exchange_Rates_Cleaned.csv",
    index=False,
    encoding="utf-8"
)

data_dictionary.to_csv(
    OUTPUT_DIR / "Data_Dictionary.csv",
    index=False,
    encoding="utf-8"
)


# ---------------------------------------------------------
# 9. CLEANING SUMMARY
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("CLEANING COMPLETE")
print("=" * 70)

print(f"\nCleaned files saved to:")
print(OUTPUT_DIR)

print("\nFiles created:")

for file in OUTPUT_DIR.iterdir():
    print(f" - {file.name}")

print("\nFinal row counts:")

print(f"Sales          : {len(sales):,}")
print(f"Products       : {len(products):,}")
print(f"Customers      : {len(customers):,}")
print(f"Stores         : {len(stores):,}")
print(f"Exchange Rates : {len(exchange_rates):,}")

print("\n" + "=" * 70)
print("READY FOR VALIDATION")
print("=" * 70)