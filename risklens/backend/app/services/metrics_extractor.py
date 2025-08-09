import pandas as pd

def parse_income_statement(sheet: pd.DataFrame) -> dict:
    """
    Parse the Income Statement from a standardized Cap IQ Pro+ export sheet.
    Returns a cleaned Income Statement DataFrame.
    """

    # 1️⃣ Drop top metadata rows that are not part of the financial table
    # Change '13' if your file has a different number of header rows
    financial_data = sheet.iloc[13:].reset_index(drop=True)

    # 2️⃣ Forward fill section headers in the first column
    financial_data.iloc[:, 0] = financial_data.iloc[:, 0].ffill()

    # 3️⃣ Rename columns so that the first column is 'Category'
    # Columns in Excel usually have years like 2021, 2022, etc.
    columns = sheet.iloc[13].tolist()
    financial_data.columns = ['Category'] + columns[1:]

    # 4️⃣ Remove the original header row inside the data
    financial_data = financial_data.iloc[1:]

    # 5️⃣ Create a mask to locate where "Income Statement" starts
    income_mask = financial_data['Category'].str.contains('Income Statement', na=False)
    income_start = income_mask.idxmax()  # Finds the first row where mask is True

    # 6️⃣ Slice only the rows after "Income Statement" section starts
    income_df = financial_data.loc[income_start+1:].dropna(how='all')

    # 7️⃣ Rename columns: First column = "Metric", rest are the year/periods
    income_df.columns = ['Metric'] + list(income_df.columns[1:])

    # 8️⃣ Optional: Filter for top 3 metrics (Revenue, Profit After Tax, EBITDA)
    # You can expand this list later
    important_metrics = ['Revenue', 'Profit After Tax', 'EBITDA']
    income_df_filtered = income_df[income_df['Metric'].isin(important_metrics)]

    return {
        "income_statement_full": income_df.reset_index(drop=True),
        "income_statement_key_metrics": income_df_filtered.reset_index(drop=True)
    }
