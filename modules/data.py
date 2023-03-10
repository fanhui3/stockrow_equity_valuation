import math
import pandas as pd

IS_columns = [
    "year",
    "Revenue",
    "Income Tax Provision",
    "Net Income Common",
    "EPS (Diluted)",
    "Shares (Diluted, Weighted)",
    "Gross Margin",
    "Net Profit Margin",
    "Free Cash Flow Margin",
    "Operating Cash Flow Margin",
    "Interest Expense (Operating)",
    "EBT",
]
BS_columns = [
    "Cash and Short Term Investments",
    "Total current assets",
    "Total non-current assets",
    "Total Assets",
    "Total current liabilities",
    "Total non-current liabilities",
    "Total liabilities",
    "Shareholders Equity (Total)",
    "Total Debt",
]
CF_columns = [
    "Operating Cash Flow",
    "Investing cash flow",
    "Issuance/Purchase of Shares",
    "Dividends Paid (Total)",
    "Financing cash flow",
    "Stock Based Compensation",
]
Metrics_columns = [
    "P/E ratio",
    "P/FCF ratio",
    "P/Operating CF",
    "P/B ratio",
    "Current Ratio",
    "Debt/Assets",
    "Debt/Equity",
    "Interest Coverage",
    "ROE",
    "ROA",
    "ROIC",
    "Free Cash Flow",
    "Book value per Share",
]


def prepare_frame(frame):
    # make first column header
    frame.columns = frame.iloc[0]
    frame = frame.iloc[1:]
    # check date column to year
    frame = frame.rename_axis("year").reset_index()
    frame["year"] = frame["year"].dt.year
    return frame


def get_data():
    # read file
    IS = pd.read_excel("./data/income.xlsx", engine="openpyxl").T
    BS = pd.read_excel("./data/balance_sheet.xlsx", engine="openpyxl").T
    CF = pd.read_excel("./data/cash_flow.xlsx", engine="openpyxl").T
    Metrics = pd.read_excel("./data/metrics.xlsx", engine="openpyxl").T

    # clean headers, set index and year
    IS = prepare_frame(IS)
    BS = prepare_frame(BS)
    CF = prepare_frame(CF)
    Metrics = prepare_frame(Metrics)

    # retain relevant columns
    IS = IS[IS.columns.intersection(IS_columns)]
    BS = BS[BS.columns.intersection(BS_columns)]
    CF = CF[CF.columns.intersection(CF_columns)]
    Metrics = Metrics[Metrics.columns.intersection(Metrics_columns)]

    # combine frames
    df = pd.concat([IS, BS, CF, Metrics], axis="columns")

    # fill na with zero
    df = df.fillna(0)

    # name column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")

    ### create needed columns

    # dividend per share
    try:
        df["dividend_per_share"] = (
            df["Dividends_Paid_(Total)"] / df["Shares_(Diluted,_Weighted)"]
        ) * -1
    except KeyError:
        df["dividend_per_share"] = 0

    # dividend payout ratio share
    try:
        df["payout_ratio"] = (
            df["Dividends_Paid_(Total)"] / df["Net_Income_Common"]
        ) * -1
    except KeyError:
        df["payout_ratio"] = 0
    df["payout_ratio"] = df["payout_ratio"].round(2)

    # represent compensation as negative event
    df["Stock_Based_Compensation"] = df["Stock_Based_Compensation"] * -1

    # represent repurchase as positive and issuance as negative
    df["Issuance/Purchase_of_Shares"] = df["Issuance/Purchase_of_Shares"] * -1

    return df


if __name__ == "__main__":
    df = get_data()
    print(df["payout_ratio"])
