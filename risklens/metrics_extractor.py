import pandas as pd

def extract_financial_highlights(xls):
    """
    Extracts financial metrics from the 'Financial Highlights' sheet.
    Returns a structured DataFrame and metadata.
    """
    sheet = xls.parse('Financial Highlights', header=None)

    # Extract metadata (company name, ticker, keys)
    company_name = sheet.iloc[1, 0]
    identifiers = sheet.iloc[2, 0]
    # Locate starting point of financial table (usually A14 == row 13 in 0-index)
    table_start_row = 13
    table_df = sheet.iloc[table_start_row:].reset_index(drop=True)

    # Forward fill categories (e.g. Balance Sheet ($000), Income Statement ($000))
    table_df.ffill(axis=0, inplace=True)

    return company_name, identifiers, table_df