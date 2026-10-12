import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# FILE LOCATION
# ---------------------------------------------------------

BASE_DIR = Path(
    r"C:\Users\HUAWEI 1\OneDrive\Documents\Global+Electronics+Retailer"
)

CLEANED_DIR = BASE_DIR / "cleaned_data"


# ---------------------------------------------------------
# LOAD CLEANED DATA
# ---------------------------------------------------------

sales = pd.read_csv(CLEANED_DIR / "Sales_Cleaned.csv")
products = pd.read_csv(CLEANED_DIR / "Products_Cleaned.csv")
customers = pd.read_csv(CLEANED_DIR / "Customers_Cleaned.csv")
stores = pd.read_csv(CLEANED_DIR / "Stores_Cleaned.csv")
exchange_rates = pd.read_csv(
    CLEANED_DIR / "Exchange_Rates_Cleaned.csv"
)

print("\n" + "=" * 70)
print("CLEANED DATA VALIDATION")
print("=" * 70)

print("\nAll cleaned datasets loaded successfully.")


# ---------------------------------------------------------
# 1. ROW COUNT VALIDATION
# ---------------------------------------------------------

print("\n--- Row Counts ---")

print(f"Sales          : {len(sales):,}")
print(f"Products       : {len(products):,}")
print(f"Customers      : {len(customers):,}")
print(f"Stores         : {len(stores):,}")
print(f"Exchange Rates : {len(exchange_rates):,}")


# ---------------------------------------------------------
# 2. PRODUCT PRICE VALIDATION
# ---------------------------------------------------------

print("\n--- Product Price Validation ---")

print("\nData Types:")
print(
    products[
        ["Unit Cost USD", "Unit Price USD"]
    ].dtypes
)

invalid_cost = pd.to_numeric(
    products["Unit Cost USD"],
    errors="coerce"
).isna().sum()

invalid_price = pd.to_numeric(
    products["Unit Price USD"],
    errors="coerce"
).isna().sum()

print(f"\nInvalid Unit Cost : {invalid_cost}")
print(f"Invalid Unit Price: {invalid_price}")


# ---------------------------------------------------------
# 3. DATE VALIDATION
# ---------------------------------------------------------

print("\n--- Date Validation ---")

sales["Order Date"] = pd.to_datetime(
    sales["Order Date"],
    errors="coerce"
)

sales["Delivery Date"] = pd.to_datetime(
    sales["Delivery Date"],
    errors="coerce"
)

print(
    "Invalid Order Dates:",
    sales["Order Date"].isna().sum()
)

print(
    "Missing Delivery Dates:",
    sales["Delivery Date"].isna().sum()
)


# ---------------------------------------------------------
# 4. CHANNEL VALIDATION
# ---------------------------------------------------------

print("\n--- Channel Validation ---")

print(
    sales["Channel"].value_counts()
)


# ---------------------------------------------------------
# 5. DUPLICATE VALIDATION
# ---------------------------------------------------------

print("\n--- Duplicate Validation ---")

print(
    "Sales duplicates:",
    sales.duplicated().sum()
)

print(
    "Products duplicates:",
    products.duplicated().sum()
)

print(
    "Customers duplicates:",
    customers.duplicated().sum()
)

print(
    "Stores duplicates:",
    stores.duplicated().sum()
)

print(
    "Exchange Rate duplicates:",
    exchange_rates.duplicated().sum()
)


# ---------------------------------------------------------
# 6. KEY VALIDATION
# ---------------------------------------------------------

print("\n--- Key Validation ---")

print(
    "CustomerKey duplicates:",
    customers["CustomerKey"].duplicated().sum()
)

print(
    "ProductKey duplicates:",
    products["ProductKey"].duplicated().sum()
)

print(
    "StoreKey duplicates:",
    stores["StoreKey"].duplicated().sum()
)


# ---------------------------------------------------------
# 7. FOREIGN KEY VALIDATION
# ---------------------------------------------------------

print("\n--- Sales Foreign Key Validation ---")

unmatched_customers = (
    ~sales["CustomerKey"].isin(customers["CustomerKey"])
).sum()

unmatched_products = (
    ~sales["ProductKey"].isin(products["ProductKey"])
).sum()

unmatched_stores = (
    ~sales["StoreKey"].isin(stores["StoreKey"])
).sum()

print("Unmatched CustomerKeys:", unmatched_customers)
print("Unmatched ProductKeys :", unmatched_products)
print("Unmatched StoreKeys   :", unmatched_stores)


# ---------------------------------------------------------
# 8. TRANSACTION VALIDATION
# ---------------------------------------------------------

print("\n--- Transaction Validation ---")

duplicate_transactions = sales.duplicated(
    subset=["Order Number", "Line Item"]
).sum()

print(
    "Duplicate Order Number + Line Item:",
    duplicate_transactions
)


# ---------------------------------------------------------
# 9. SPECIAL NULL VALIDATION
# ---------------------------------------------------------

print("\n--- Expected NULL Validation ---")

online_square_meters = stores.loc[
    stores["StoreKey"] == 0,
    "Square Meters"
].isna().sum()

missing_state_codes = customers[
    "State Code"
].isna().sum()

in_store_missing_delivery = sales.loc[
    sales["Channel"] == "In-Store",
    "Delivery Date"
].isna().sum()

online_missing_delivery = sales.loc[
    sales["Channel"] == "Online",
    "Delivery Date"
].isna().sum()

print(
    "Online Store Square Meters NULL:",
    online_square_meters
)

print(
    "Customer State Code NULL:",
    missing_state_codes
)

print(
    "In-Store missing Delivery Dates:",
    in_store_missing_delivery
)

print(
    "Online missing Delivery Dates:",
    online_missing_delivery
)


# ---------------------------------------------------------
# COMPLETE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)


print("\n" + "=" * 70)
print("INVALID PRODUCT PRICE INVESTIGATION")
print("=" * 70)

invalid_products = products[
    products["Unit Cost USD"].isna() |
    products["Unit Price USD"].isna()
]

print(f"\nProducts with at least one invalid price: {len(invalid_products)}")

print(
    invalid_products[
        [
            "ProductKey",
            "Product Name",
            "Unit Cost USD",
            "Unit Price USD",
            "Category",
            "Subcategory"
        ]
    ].to_string(index=False)
)

print("\n" + "=" * 70)
print("RAW PRODUCT PRICE CHECK")
print("=" * 70)

raw_products = pd.read_csv(
    BASE_DIR / "Products.csv",
    encoding="cp1252"
)

affected_keys = invalid_products["ProductKey"]

raw_affected = raw_products[
    raw_products["ProductKey"].isin(affected_keys)
]

print(
    raw_affected[
        [
            "ProductKey",
            "Product Name",
            "Unit Cost USD",
            "Unit Price USD"
        ]
    ].to_string(index=False)
)