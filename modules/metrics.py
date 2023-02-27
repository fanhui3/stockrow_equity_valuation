import data
import pandas
import numpy as np


def shares(frame):
    frame = frame.iloc[0]
    shares = int(frame["Shares_(Diluted,_Weighted)"])
    return shares


def book_value(frame):
    frame = frame.iloc[0]
    book_value = frame["Book_value_per_Share"]
    return book_value


def debt_cost(frame):
    frame = frame.iloc[0]
    try:
        debt_cost = frame["Interest_Expense_(Operating)"] / frame["Total_Debt"]
    except KeyError:
        debt_cost = 0
    if np.isnan(debt_cost):
        return 0
    return debt_cost


def tax_rate(frame):
    frame = frame.iloc[0]
    tax_rate = frame["Income_Tax_Provision"] / frame["EBT"]
    return tax_rate


def debt_weight(frame, current_share_price=1):
    frame = frame.iloc[0]
    debt = frame["Total_Debt"]
    market_cap = frame["Shares_(Diluted,_Weighted)"] * current_share_price
    return debt / (debt + market_cap)


def equity_weight(frame, current_share_price=1):
    frame = frame.iloc[0]
    debt = frame["Total_Debt"]
    market_cap = frame["Shares_(Diluted,_Weighted)"] * current_share_price
    return market_cap / (debt + market_cap)


def equity_cost(market_return_rate=0.1, risk_free_rate=0.02, beta=1):
    equity_cost = risk_free_rate + (beta * (market_return_rate - risk_free_rate))
    return equity_cost


def wacc(
    frame, current_share_price, market_return_rate=0.1, risk_free_rate=0.02, beta=1
):
    debtweight = debt_weight(frame, current_share_price)
    equityweight = equity_weight(frame, current_share_price)
    equitycost = equity_cost(market_return_rate, risk_free_rate, beta)
    debtcost = debt_cost(frame)
    taxrate = tax_rate(frame)
    wacc = ((equityweight * equitycost) + (debtweight * debtcost * (1 - taxrate))) + 1
    return wacc


if __name__ == "__main__":
    df = data.get_data()
    print(df["Total_Debt"])
