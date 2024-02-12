import math
import pandas as pd
import os
import numpy as np

invalid_data = ["-", "—"]

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
# get the file path of one folder up
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def prepare_frame(frame):
    # set first row as header
    frame.columns = frame.iloc[0]
    frame = frame[1:]

    # get the year columns
    frame = frame.rename_axis("year").reset_index()
    # # current date format is Sep'14, replace ' and month before with "20"
    frame["year"] = frame["year"].apply(lambda x: "20" + x.split("'")[1])
    return frame


def get_data():
    # read file
    IS = pd.read_excel(
        f"{file_path}/data/full_data.xlsx", sheet_name="Income Statement, A"
    ).T
    BS = pd.read_excel(
        f"{file_path}/data/full_data.xlsx", sheet_name="Balance Sheet, A"
    ).T
    CF = pd.read_excel(f"{file_path}/data/full_data.xlsx", sheet_name="Cash Flow, A").T
    METRICS = pd.read_excel(
        f"{file_path}/data/full_data.xlsx", sheet_name="Metrics Ratios, A"
    ).T

    # clean headers, set index and year
    IS = prepare_frame(IS)
    BS = prepare_frame(BS)
    CF = prepare_frame(CF)
    METRICS = prepare_frame(METRICS)

    # retain relevant columns
    IS = IS[IS.columns.intersection(IS_columns)]
    BS = BS[BS.columns.intersection(BS_columns)]
    CF = CF[CF.columns.intersection(CF_columns)]
    METRICS = METRICS[METRICS.columns.intersection(Metrics_columns)]

    # combine frames
    df = pd.concat([IS, BS, CF, METRICS], axis="columns")

    # if cell contains invalid data, replace with NaN
    for column in df.columns:
        df[column] = df[column].apply(lambda x: np.nan if x in invalid_data else x)
    df = df.fillna(0)

    # name column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")

    # convert year column to int
    df["year"] = df["year"].astype(int)

    # convert all other columns to float
    for col in df.columns[1:]:
        df[col] = df[col].astype(float)

    # sort df by year in descending order
    df = df.sort_values(by="year", ascending=False)

    # filter out the years with value 0 from merging different dataframes
    df = df[df["year"] != 0]

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
    breakpoint()
    # df = get_data()
    # print(df["payout_ratio"])
