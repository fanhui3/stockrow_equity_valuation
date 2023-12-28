import streamlit as st
import pandas as pd

# from modules import data
# from modules import metrics
# from modules import valuation
# from modules import visualisation
# from modules import csv_dowloader
import modules.data as data
import modules.metrics as metrics
import modules.valuation as valuation
import modules.visualisation as visualisation
import modules.csv_dowloader as csv_dowloader
import pickle
import os

file_path = os.path.join(os.path.dirname(__file__), "dataframe.pkl")


# download data function
def download_data(ticker):
    print("Downloading CSV for ticker:", ticker)
    csv_dowloader.download_csv(ticker)
    updated_df = data.get_data()
    print("Updated DataFrame shape:", updated_df.shape)
    return updated_df


st.title("Stock Valuation App")
st.sidebar.title("Settings")

ticker = st.sidebar.text_input("enter ticker symbol", value="aapl")
CURRENT_PRICE = st.sidebar.number_input(
    "CURRENT_PRICE",
)
BETA = st.sidebar.number_input("BETA", value=1.2)
years_to_forecast = st.sidebar.number_input(
    "Number of past years to project growth", value=4
)
CAP_GROWTH = st.sidebar.number_input("CAP_GROWTH", value=1.15)
MARKET_RETURN = st.sidebar.number_input("Expected annual market return", value=0.1)
RISK_FREE_RETURN = st.sidebar.number_input("Current risk free return", value=0.035)

# buttons
st.sidebar.write("Operations")
collect = st.sidebar.button("Download Data")
profit = st.sidebar.button("See Profitability")
health = st.sidebar.button("See Financial Health")
value = st.sidebar.button("See Valuation")
test = st.sidebar.button("Test")

if collect:
    df = download_data(ticker=ticker)
    df.to_pickle(file_path)

if test:
    df = pd.read_pickle(file_path)
    st.write(df)

#
