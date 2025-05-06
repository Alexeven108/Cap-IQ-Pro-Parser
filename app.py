import streamlit as st
from risklens.file_handler import upload_file
import pandas as pd
from risklens.metrics_extractor import parse_financial_highlights

def main():
    # App Title
    st.title("🔎 RiskLens - Financial Risk Analyzer")

    # Upload Excel file
    df = upload_file()

    # If DataFrame exists, show a preview
    if df is not None:
        st.subheader("📄 Uploaded Data Preview")
        st.dataframe(df.head())

        # Placeholder for next steps
        st.subheader("Analysis Section Coming Soon...")
        st.info("You'll be able to run financial metrics analysis here.")

if __name__ == "__main__":
    main()


# Load Excel
xls = pd.ExcelFile("sample_capiq_data.")

# Load sheet
sheet1 = xls.parse(xls.sheet_names[0], header=None)

# Analyze
results = parse_financial_highlights(sheet1)

# Preview
print("Balance Sheet:")
print(results['balance_sheet'].head())

print("Income Statement:")
print(results['income_statement'].head())
