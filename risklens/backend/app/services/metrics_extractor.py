import pandas as pd

def parse_income_statement(file_path: str) -> dict:
    """
    Parse the Income Statement from a standardized Cap IQ Pro+ export.
    Reads ONLY the 'Income Statement' sheet and extracts key metrics + ratios.
    """

    # 1️⃣ Read only the Income Statement sheet
    df = pd.read_excel(file_path, sheet_name="Income Statement")

    # 2️⃣ Clean the data
    df.columns = df.columns.str.strip()  # Remove extra spaces in column names
    df = df.dropna(how='all')  # Remove empty rows

    # 3️⃣ Extract core financials (update names based on your Excel export)
    revenue = df.loc[df['Unnamed: 0'] == 'Total Revenue'].iloc[:, 1:]
    cogs = df.loc[df['Unnamed: 0'] == 'Cost Of Goods Sold'].iloc[:, 1:]
    gross_profit = df.loc[df['Unnamed: 0'] == 'Gross Profit'].iloc[:, 1:]
    operating_income = df.loc[df['Unnamed: 0'] == 'Operating Income'].iloc[:, 1:]
    net_income = df.loc[df['Unnamed: 0'] == 'Net Income'].iloc[:, 1:]
    ebitda = df.loc[df['Unnamed: 0'] == 'EBITDA'].iloc[:, 1:]
    sgna = df.loc[df['Unnamed: 0'].str.contains("Selling General", na=False)].iloc[:, 1:]
    payroll = df.loc[df['Unnamed: 0'].str.contains("Total Payroll", na=False)].iloc[:, 1:]
    income_tax = df.loc[df['Unnamed: 0'].str.contains("Income Tax Expense", na=False)].iloc[:, 1:]
    ebt = df.loc[df['Unnamed: 0'] == 'EBT Incl. Unusual Items'].iloc[:, 1:]

    # 4️⃣ Calculate metrics
    gross_margin = gross_profit / revenue
    operating_margin = operating_income / revenue
    net_margin = net_income / revenue
    ebitda_margin = ebitda / revenue
    cogs_ratio = cogs / revenue
    sgna_ratio = sgna / revenue
    payroll_ratio = payroll / revenue
    yoy_revenue_growth = revenue.pct_change(axis=1)
    effective_tax_rate = income_tax / ebt

    # 5️⃣ Return all data in a dictionary for flexibility
    return {
        "raw_income_statement": df,
        "metrics": {
            "Revenue": revenue,
            "Gross Profit": gross_profit,
            "Operating Income": operating_income,
            "Net Income": net_income,
            "EBITDA": ebitda,
        },
        "ratios": {
            "Gross Margin": gross_margin,
            "Operating Margin": operating_margin,
            "Net Margin": net_margin,
            "EBITDA Margin": ebitda_margin,
            "COGS Ratio": cogs_ratio,
            "SG&A Ratio": sgna_ratio,
            "Payroll Ratio": payroll_ratio,
            "YoY Revenue Growth": yoy_revenue_growth,
            "Effective Tax Rate": effective_tax_rate
        }
    }

# Example usage:
# results = parse_income_statement("revolut_income.xlsx")
# print(results["ratios"]["Gross Margin"])
