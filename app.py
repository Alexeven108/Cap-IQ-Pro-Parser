import streamlit as st
from risklens.file_handler import upload_file

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
