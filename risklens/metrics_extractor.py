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