import pandas as pd
import streamlit as st


def upload_file():
    """
    Handles file upload via Streamlit and returns a pandas DataFrame.
    """
    uploaded_file = st.file_uploader("📂 Upload your Excel file (.xlsx)", type=["xlsx"])

    if uploaded_file is not None:
        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(uploaded_file, engine='openpyxl')

            # Basic cleaning: strip whitespace from headers
            df.columns = df.columns.str.strip()

            st.success("✅ File successfully uploaded and loaded!")
            return df

        except Exception as e:
            st.error(f"❌ Error reading the file: {e}")
            return None
    else:
        st.info("👆 Please upload an Excel file to get started.")
        return None
