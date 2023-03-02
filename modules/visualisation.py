import pandas as pd
import matplotlib.pyplot as plt  # pyplot package under the matplotlib package
import seaborn as sns
import data

plt.style.use("ggplot")


def visualise_profitability(frame):
    axis = list(frame["year"])
    axis = sorted(axis)

    fig, axes = plt.subplots(2, 3, figsize=(20, 12))

    # various cashflows
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

    # FCF vs debt
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

    # OCF vs Income
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

    # dividends
    axes[1, 0].bar(frame["year"], frame["dividend_per_share"], color="skyblue")
    axes[1, 0].plot(frame["year"], frame["payout_ratio"], color="black")
    axes[1, 0].tick_params(axis="x", rotation=45)
    axes[1, 0].set(title="Dividends")
    for index in range(len(frame["year"])):
        axes[1, 0].text(
            frame["year"][index],
            frame["payout_ratio"][index],
            frame["payout_ratio"][index],
            size=12,
        )

    # ROE, ROA, ROIC
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

    # OCF, FCF, Income Margins
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


if __name__ == "__main__":
    frame = data.get_data()
    visualise_profitability(frame=frame)
