import pandas as pd
import matplotlib.pyplot as plt  # pyplot package under the matplotlib package
import seaborn as sns
import data

plt.style.use("ggplot")


def visualise_profitability(frame):
    frame = frame.sort_values(by="year", ascending=True)
    axis = list(frame["year"])
    axis = sorted(axis)

    fig, axes = plt.subplots(2, 3, figsize=(20, 12))

    # cashflow
    cashflow_df = frame[
        ["year", "Operating_Cash_Flow", "Investing_cash_flow", "Financing_cash_flow"]
    ]
    cashflow_df = cashflow_df.melt(
        id_vars="year", var_name="cashflow", value_name="amount"
    )
    sns.barplot(
        x="year",
        y="amount",
        data=cashflow_df,
        hue="cashflow",
        palette=["orange", "blue", "red"],
        order=axis,
        ax=axes[0, 0],
    )
    axes[0, 0].set(title="Cashflows")
    axes[0, 0].set(xlabel=None)
    axes[0, 0].set(ylabel=None)

    # FCF and debt
    fcf_df = frame[["year", "Free_Cash_Flow", "Total_Debt"]]
    fcf_df = fcf_df.melt(id_vars="year", var_name="cashflow", value_name="amount")
    sns.barplot(
        x="year",
        y="amount",
        data=fcf_df,
        hue="cashflow",
        palette=["green", "red"],
        order=axis,
        ax=axes[0, 1],
    )
    axes[0, 1].set(title="Free CF vs Debt")
    axes[0, 1].set(xlabel=None)
    axes[0, 1].set(ylabel=None)

    # cashflow vs income
    cashflow_income = frame[["year", "Operating_Cash_Flow", "Net_Income_Common"]]
    cashflow_income = cashflow_income.melt(
        id_vars="year", var_name="source", value_name="amount"
    )
    sns.barplot(
        x="year",
        y="amount",
        data=cashflow_income,
        hue="source",
        palette=["orange", "tan"],
        order=axis,
        ax=axes[0, 2],
    )
    axes[0, 2].set(title="Operating CF vs Net Income")
    axes[0, 2].set(xlabel=None)
    axes[0, 2].set(ylabel=None)

    # dividends
    axes[1, 0].bar(
        frame["year"],
        frame["dividend_per_share"],
        color="skyblue",
        label="Dividends Per Share",
    )
    ax2 = axes[1, 0].twinx()
    ax2.plot(frame["year"], frame["payout_ratio"], color="black", label="Payout Ratio")
    ax2.tick_params(axis="x", rotation=45)
    axes[1, 0].set(title="Dividends")
    for index in range(len(frame["year"])):
        axes[1, 0].text(
            frame["year"][index],
            frame["payout_ratio"][index],
            frame["payout_ratio"][index],
            size=12,
        )
    axes[1, 0].legend(loc=3)
    ax2.legend(loc=3, bbox_to_anchor=(0.0, 0.1, 0.0, 0.5))
    axes[1, 0].set(xlabel=None)
    axes[1, 0].set(ylabel=None)
    ax2.set(xlabel=None)
    ax2.set(ylabel=None)

    # Returns
    returns = frame[["year", "ROE", "ROA", "ROIC"]]
    returns = returns.melt(id_vars="year", var_name="returns", value_name="amount")
    sns.lineplot(
        x="year",
        y="amount",
        data=returns,
        hue="returns",
        palette=["orange", "black", "blue"],
        ax=axes[1, 1],
    )
    axes[1, 1].set(title="Returns")
    axes[1, 1].set(xlabel=None)
    axes[1, 1].set(ylabel=None)

    # margins
    margins = frame[
        [
            "year",
            "Operating_Cash_Flow_Margin",
            "Free_Cash_Flow_Margin",
            "Net_Profit_Margin",
        ]
    ]
    margins = margins.melt(id_vars="year", var_name="margins", value_name="amount")
    sns.lineplot(
        x="year",
        y="amount",
        data=margins,
        hue="margins",
        palette=["orange", "green", "tan"],
        ax=axes[1, 2],
    )
    axes[1, 2].set(title="Margin")
    axes[1, 2].legend(loc="lower left")
    axes[1, 2].set(xlabel=None)
    axes[1, 2].set(ylabel=None)


def visualise_financial_health(frame):
    frame = frame.sort_values(by="year", ascending=True)
    axis = list(frame["year"])
    axis = sorted(axis)

    fig2, axes = plt.subplots(2, 3, figsize=(20, 12))

    # Cash vs Debt vs total
    balancesheet_prop = frame[
        ["year", "Cash_and_Short_Term_Investments", "Total_Debt", "Total_Assets"]
    ]
    balancesheet_prop = balancesheet_prop.melt(
        id_vars="year", var_name="source", value_name="amount"
    )
    sns.barplot(
        x="year",
        y="amount",
        data=balancesheet_prop,
        hue="source",
        palette=["green", "red", "black", "black"],
        order=axis,
        ax=axes[0, 0],
    )
    axes[0, 0].set(title="Cash, Debt and Total Asset")
    axes[0, 0].set(xlabel=None)
    axes[0, 0].set(ylabel=None)

    # proportion of BS
    balancesheet_df = frame[
        [
            "year",
            "Shareholders_Equity_(Total)",
            "Total_current_liabilities",
            "Total_non-current_liabilities",
        ]
    ]
    balancesheet_df = balancesheet_df.set_index("year").sort_index()
    balancesheet_df = balancesheet_df.div(balancesheet_df.sum(axis=1), axis=0)
    balancesheet_df.plot(
        kind="bar", stacked=True, color=["blue", "brown", "red"], ax=axes[0, 1]
    )
    axes[0, 1].set(xlabel=None)
    axes[0, 1].set(ylabel=None)
    axes[0, 1].set(title="Balancesheet Proportion")
    axes[0, 1].set(xlabel=None)
    axes[0, 1].set(ylabel=None)

    # Current ration and Debt/Equity
    bs_ratio_df = frame[["year", "Current_Ratio", "Debt/Equity"]]
    bs_ratio_df = bs_ratio_df.melt(
        id_vars="year", var_name="ratio", value_name="amount"
    )
    sns.lineplot(
        x=bs_ratio_df["year"],
        y=bs_ratio_df["amount"],
        hue=bs_ratio_df["ratio"],
        palette=["blue", "red"],
        ax=axes[0, 2],
    )
    sns.lineplot(
        x=bs_ratio_df["year"], y=1, color="black", linestyle="--", ax=axes[0, 2]
    )
    axes[0, 2].set(title="Current Ratio and Debt to Equity")
    axes[0, 2].set(xlabel=None)
    axes[0, 2].set(ylabel=None)

    # interest coverage
    axes[1, 0].plot(
        frame["year"],
        frame["Interest_Coverage"],
        color="red",
        label="EBT/Interest Expense",
    )
    axes[1, 0].axhline(y=1, color="black", linestyle="--")
    axes[1, 0].set(title="Interest Coverage")
    axes[1, 0].legend(loc=3)
    axes[1, 0].set(xlabel=None)
    axes[1, 0].set(ylabel=None)

    # share dilution
    axes[1, 1].bar(
        frame["year"],
        frame["Stock_Based_Compensation"],
        color="red",
        label="Stock-based Compensation ($)",
    )
    axes[1, 1].bar(
        frame["year"],
        frame["Issuance/Purchase_of_Shares"],
        color="orange",
        label="Stock Repurchase / Issuance ($)",
    )
    ax2 = axes[1, 1].twinx()
    ax2.plot(
        frame["year"],
        frame["Shares_(Diluted,_Weighted)"],
        color="black",
        label="Share Count",
    )
    ax2.tick_params(axis="x", rotation=45)
    axes[1, 1].set(title="Share Dilution")
    axes[1, 1].legend(loc=3)
    ax2.legend(loc=3, bbox_to_anchor=(0.0, 0.1, 0.0, 0.5))
    axes[1, 1].set(xlabel=None)
    axes[1, 1].set(ylabel=None)


if __name__ == "__main__":
    frame = data.get_data()
    visualise_financial_health(frame=frame)
    plt.show()
