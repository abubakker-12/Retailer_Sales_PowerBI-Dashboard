import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# 1. SETUP
# ============================================================

print("=" * 70)
print("GLOBAL ELECTRONICS RETAILER - DATA AUDIT")
print("=" * 70)

base_path = Path(__file__).parent

# Raw data files
file_paths = {
    "Sales": base_path / "Sales.csv",
    "Products": base_path / "Products.csv",
    "Customers": base_path / "Customers.csv",
    "Stores": base_path / "Stores.csv",
    "Exchange Rates": base_path / "Exchange_Rates.csv",
    "Data Dictionary": base_path / "Data_Dictionary.csv"
}


# ============================================================
# 2. LOAD RAW DATA
# ============================================================

sales = pd.read_csv(file_paths["Sales"], encoding="cp1252")
products = pd.read_csv(file_paths["Products"], encoding="cp1252")
customers = pd.read_csv(file_paths["Customers"], encoding="cp1252")
stores = pd.read_csv(file_paths["Stores"], encoding="cp1252")
exchange_rates = pd.read_csv(file_paths["Exchange Rates"], encoding="cp1252")
data_dictionary = pd.read_csv(file_paths["Data Dictionary"], encoding="cp1252")

datasets = {
    "Sales": sales,
    "Products": products,
    "Customers": customers,
    "Stores": stores,
    "Exchange Rates": exchange_rates,
    "Data Dictionary": data_dictionary
}

print("\nAll datasets loaded successfully.")


# ============================================================
# 3. DATASET OVERVIEW
# ============================================================

print("\n" + "=" * 70)
print("1. DATASET OVERVIEW")
print("=" * 70)

for name, df in datasets.items():
    print(
        f"{name:<20} "
        f"Rows: {len(df):>8,} | "
        f"Columns: {len(df.columns):>3}"
    )


# ============================================================
# 4. COLUMN-LEVEL DATA QUALITY
# ============================================================

print("\n" + "=" * 70)
print("2. COLUMN-LEVEL DATA QUALITY")
print("=" * 70)

for name, df in datasets.items():

    print(f"\n--- {name} ---")

    audit = pd.DataFrame({
        "Data Type": df.dtypes.astype(str),
        "Missing": df.isna().sum(),
        "Missing %": (df.isna().mean() * 100).round(2),
        "Unique": df.nunique()
    })

    print(audit.to_string())


# ============================================================
# 5. EXACT DUPLICATES
# ============================================================

print("\n" + "=" * 70)
print("3. EXACT DUPLICATE AUDIT")
print("=" * 70)

for name, df in datasets.items():

    duplicates = df.duplicated().sum()

    print(f"{name:<20} Exact duplicates: {duplicates:,}")


# ============================================================
# 6. DIMENSION KEY AUDIT
# ============================================================

print("\n" + "=" * 70)
print("4. DIMENSION KEY AUDIT")
print("=" * 70)

dimension_keys = {
    "Customers": ("CustomerKey", customers),
    "Products": ("ProductKey", products),
    "Stores": ("StoreKey", stores)
}

for name, (key, df) in dimension_keys.items():

    duplicate_keys = df[key].duplicated().sum()

    null_keys = df[key].isna().sum()

    print(
        f"{name:<15} "
        f"Duplicate keys: {duplicate_keys:,} | "
        f"Null keys: {null_keys:,}"
    )


# ============================================================
# 7. SALES FOREIGN KEY AUDIT
# ============================================================

print("\n" + "=" * 70)
print("5. SALES FOREIGN KEY AUDIT")
print("=" * 70)

relationships = {
    "CustomerKey": customers["CustomerKey"],
    "ProductKey": products["ProductKey"],
    "StoreKey": stores["StoreKey"]
}

for key, valid_keys in relationships.items():

    unmatched = (~sales[key].isin(valid_keys)).sum()

    print(
        f"Sales → {key:<12} "
        f"Unmatched rows: {unmatched:,}"
    )


# ============================================================
# 8. SALES TRANSACTION KEY
# ============================================================

print("\n" + "=" * 70)
print("6. SALES TRANSACTION KEY AUDIT")
print("=" * 70)

transaction_duplicates = sales.duplicated(
    subset=["Order Number", "Line Item"]
).sum()

print(
    "Duplicate Order Number + Line Item combinations:",
    transaction_duplicates
)


# ============================================================
# 9. SALES CHANNEL AUDIT
# ============================================================

print("\n" + "=" * 70)
print("7. SALES CHANNEL AUDIT")
print("=" * 70)

sales["Channel"] = np.where(
    sales["StoreKey"] == 0,
    "Online",
    "In-Store"
)

channel_summary = (
    sales.groupby("Channel")
    .agg(
        Transaction_Lines=("Order Number", "count"),
        Orders=("Order Number", "nunique"),
        Customers=("CustomerKey", "nunique"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)

print(channel_summary.to_string(index=False))


# ============================================================
# 10. STOREKEY VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("8. STOREKEY VALIDATION")
print("=" * 70)

print("\nStoreKey = 0 record:")

print(
    stores[stores["StoreKey"] == 0]
    .to_string(index=False)
)


# ============================================================
# 11. DATE AUDIT
# ============================================================

print("\n" + "=" * 70)
print("9. DATE AUDIT")
print("=" * 70)

order_dates = pd.to_datetime(
    sales["Order Date"],
    errors="coerce"
)

delivery_dates = pd.to_datetime(
    sales["Delivery Date"],
    errors="coerce"
)

print("\nOrder Date")
print("Minimum:", order_dates.min())
print("Maximum:", order_dates.max())
print("Invalid:", order_dates.isna().sum())

print("\nDelivery Date")
print("Minimum:", delivery_dates.min())
print("Maximum:", delivery_dates.max())
print("Missing / Invalid:", delivery_dates.isna().sum())


# Delivery before order

valid_delivery = delivery_dates.notna()

delivery_before_order = (
    delivery_dates[valid_delivery]
    < order_dates[valid_delivery]
).sum()

print("\nDelivery before Order:", delivery_before_order)


# Delivery duration

delivery_days = (
    delivery_dates - order_dates
).dt.days

print("\nDelivery Duration")
print("Minimum days:", delivery_days.min())
print("Maximum days:", delivery_days.max())
print("Average days:", round(delivery_days.mean(), 2))
print("Median days:", delivery_days.median())


# ============================================================
# 12. DELIVERY DATE BY CHANNEL
# ============================================================

print("\n" + "=" * 70)
print("10. DELIVERY DATE vs SALES CHANNEL")
print("=" * 70)

delivery_channel = (
    sales.groupby("Channel")
    .agg(
        Total=("Order Number", "count"),
        Missing_Delivery=(
            "Delivery Date",
            lambda x: x.isna().sum()
        ),
        Available_Delivery=(
            "Delivery Date",
            lambda x: x.notna().sum()
        )
    )
    .reset_index()
)

delivery_channel["Missing %"] = (
    delivery_channel["Missing_Delivery"]
    / delivery_channel["Total"]
    * 100
).round(2)

print(delivery_channel.to_string(index=False))


# ============================================================
# 13. NUMERIC DATA AUDIT
# ============================================================

print("\n" + "=" * 70)
print("11. NUMERIC DATA AUDIT")
print("=" * 70)

numeric_columns = {
    "Sales": ["Quantity"],
    "Products": ["Unit Cost USD", "Unit Price USD"],
    "Stores": ["Square Meters"],
    "Exchange Rates": ["Exchange"]
}

for dataset_name, columns in numeric_columns.items():

    df = datasets[dataset_name]

    print(f"\n--- {dataset_name} ---")

    for column in columns:

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        print(
            f"{column:<20} "
            f"Min: {numeric_values.min()} | "
            f"Max: {numeric_values.max()} | "
            f"Invalid: {numeric_values.isna().sum()}"
        )


# ============================================================
# 14. CATEGORICAL VALUE AUDIT
# ============================================================

print("\n" + "=" * 70)
print("12. CATEGORICAL VALUE AUDIT")
print("=" * 70)

categorical_columns = {
    "Sales": ["Currency Code"],
    "Products": ["Brand", "Category", "Subcategory"],
    "Customers": ["Gender", "Country", "Continent"],
    "Stores": ["Country"]
}

for dataset_name, columns in categorical_columns.items():

    df = datasets[dataset_name]

    print(f"\n--- {dataset_name} ---")

    for column in columns:

        values = df[column].dropna().unique()

        print(
            f"{column:<20} "
            f"{len(values)} unique values"
        )

        print(
            "Values:",
            list(values)
        )


# ============================================================
# 15. CURRENCY AUDIT
# ============================================================

print("\n" + "=" * 70)
print("13. CURRENCY AUDIT")
print("=" * 70)

print("\nSales currencies:")
print(
    sales["Currency Code"]
    .value_counts()
    .to_string()
)

print("\nExchange-rate currencies:")
print(
    exchange_rates["Currency"]
    .value_counts()
    .to_string()
)


# ============================================================
# 16. EXCHANGE RATE DATE AUDIT
# ============================================================

print("\n" + "=" * 70)
print("14. EXCHANGE RATE DATE AUDIT")
print("=" * 70)

exchange_dates = pd.to_datetime(
    exchange_rates["Date"],
    errors="coerce"
)

print("Minimum date:", exchange_dates.min())
print("Maximum date:", exchange_dates.max())
print("Invalid dates:", exchange_dates.isna().sum())

print("\nExchange rates per currency:")

print(
    exchange_rates.groupby("Currency")
    .agg(
        Rows=("Currency", "count"),
        Unique_Dates=("Date", "nunique")
    )
    .to_string()
)


# ============================================================
# 17. CUSTOMER DATA AUDIT
# ============================================================

print("\n" + "=" * 70)
print("15. CUSTOMER DATA AUDIT")
print("=" * 70)

print("\nCustomers per country:")
print(
    customers["Country"]
    .value_counts()
    .to_string()
)

print("\nMissing customer fields:")

customer_missing = (
    customers.isna().sum()
    .sort_values(ascending=False)
)

print(customer_missing[customer_missing > 0].to_string())


# ============================================================
# 18. PRODUCT DATA AUDIT
# ============================================================

print("\n" + "=" * 70)
print("16. PRODUCT DATA AUDIT")
print("=" * 70)

print("\nProducts by category:")

print(
    products["Category"]
    .value_counts()
    .to_string()
)

print("\nProducts by brand:")

print(
    products["Brand"]
    .value_counts()
    .to_string()
)


# ============================================================
# 19. STORE DATA AUDIT
# ============================================================

print("\n" + "=" * 70)
print("17. STORE DATA AUDIT")
print("=" * 70)

print("\nStores by country:")

print(
    stores["Country"]
    .value_counts()
    .to_string()
)

print("\nMissing store fields:")

store_missing = (
    stores.isna().sum()
    .sort_values(ascending=False)
)

print(store_missing[store_missing > 0].to_string())


# ============================================================
# 20. FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)

print("""
No data has been cleaned or modified in the source CSV files.

This audit is for identifying:
- Data-quality issues
- Missing values
- Duplicate records
- Key integrity
- Date problems
- Currency issues
- Channel structure
- Business-rule anomalies

The cleaning stage will begin only after reviewing these results.
""")

print("\n" + "=" * 70)
print("PROBLEM VALUE INSPECTION")
print("=" * 70)

print("\n--- Product Price Examples ---")
print(
    products[
        ["Product Name", "Unit Cost USD", "Unit Price USD"]
    ].head(10).to_string(index=False)
)

print("\n--- Customers with Missing State Code ---")
print(
    customers[customers["State Code"].isna()]
    .to_string(index=False)
)

print("\n--- Store with Missing Square Meters ---")
print(
    stores[stores["Square Meters"].isna()]
    .to_string(index=False)
)