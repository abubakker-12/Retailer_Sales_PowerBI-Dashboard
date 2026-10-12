# Global Electronics Retailer Analytics Dashboard 📊

An end-to-end data analytics project featuring a robust **Python data-cleaning pipeline** and an interactive **Power BI Executive Dashboard**. This project transforms raw retail operational data across customer profiles, global store metrics, dynamic products, exchange rates, and historical sales into actionable commercial insights.

---

## 🛠️ Tech Stack & Workflow
*   **Data Extraction & Cleaning:** Python (Pandas, Numpy)
*   **Pipeline Validation:** Python automated validation scripts
*   **Database/Storage:** Structured CSV architecture
*   **Data Modeling & BI Visualization:** Microsoft Power BI Desktop (DAX, Power Query)

---

## 📁 Repository Structure
```text
├── 📁 data/                  # Raw operational source sheets (.csv)
├── 📁 cleaned_data/          # Output of the Python ETL data pipeline
├── 📁 icons/                 # Custom UI/UX dashboard navigation elements
├── 📄 electronics_retailer_cleaning.py       # Python script for missing values & formatting
├── 📄 electronics_retailer_validation.py     # Data integrity check script
├── 📄 electronics_retailer_analysis.py       # Python-driven exploratory data analysis (EDA)
├── 📄 electronics_retailer_Dashboard.pbix    # Core interactive Power BI Dashboard
└── 📄 Global_Electronics_Retailer_BI_Project_Documentation.pdf   # Full business report
```

---

## ⚙️ Data Pipeline & Data Engineering (Python)
Before loading the data into Power BI, a modular Python architecture was built to ensure data reliability:
1.  **Data Cleansing (`electronics_retailer_cleaning.py`):** Fixed inconsistent date formats, handled missing values, standardized string fields, and removed duplicates across Customer, Products, and Sales datasets.
2.  **Integrity Validation (`electronics_retailer_validation.py`):** Verified primary key unique integrity, ensured exchange rate conversions aligned chronologically, and flagged anomalies.
3.  **Outputs:** Pushed structurally sound datasets to the `/cleaned_data` folder to optimize Power BI data refresh performance and minimize Power Query transformation overhead.

---

## 📊 Power BI Dashboard Architecture & Key Features
The interactive dashboard provides business leaders with an executive-level view of retail performance:

*   **Dynamic Currency Conversion:** Leveraged DAX modeling to dynamically adjust multi-national sales figures using the `Exchange_Rates` metrics against a baseline currency.
*   **Customer Segmentation:** Clear breakdowns of customer demographics, age groupings, and purchasing frequencies.
*   **Product Performance Metrics:** Profitability margins, inventory turns, and product type popularity charts.
*   **Global Stores Insight:** Visualizes store location metrics and sales margins across international markets.
*   **Intuitive UI/UX:** Built using custom navigation icons for seamless multi-page switching (Sales Insights vs Product Insights vs Customer View).

---

## 🚀 How To Run This Project
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/abubakker-12/Retailer_Sales_PowerBI-Dashboard.git
   ```
2. Review the data transformations by opening and executing `electronics_retailer_cleaning.py`.
3. Open `electronics_retailer_Dashboard.pbix` in **Power BI Desktop** to explore the interactive visual models, fields, and custom DAX measures.
