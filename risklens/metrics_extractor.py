import pandas as pd

def parse_financial_highlights(sheet: pd.DataFrame) -> dict:
    """
    Parse financial highlights from a standardized Cap IQ Pro+ export sheet.
    Returns cleaned Balance Sheet and Income Statement DataFrames.
    """
    # Drop top metadata rows
    financial_data = sheet.iloc[13:].reset_index(drop=True)

    # Forward fill section headers
    financial_data.iloc[:, 0] = financial_data.iloc[:, 0].ffill()

    # Rename columns
    columns = sheet.iloc[13].tolist()
    financial_data.columns = ['Category'] + columns[1:]

    # Drop the original header row
    financial_data = financial_data.iloc[1:]

    # Split into sections
    balance_mask = financial_data['Category'].str.contains('Balance Sheet', na=False)
    income_mask = financial_data['Category'].str.contains('Income Statement', na=False)

    balance_start = balance_mask.idxmax()
    income_start = income_mask.idxmax()

    balance_df = financial_data.loc[balance_start+1:income_start-1].dropna(how='all')
    income_df = financial_data.loc[income_start+1:].dropna(how='all')

    # Clean headers
    balance_df.columns = ['Metric'] + list(balance_df.columns[1:])
    income_df.columns = ['Metric'] + list(income_df.columns[1:])

    return {
        "balance_sheet": balance_df.reset_index(drop=True),
        "income_statement": income_df.reset_index(drop=True)
    }

#top 3 metrics to try, revenue, profit after tax, EBITDA calculator