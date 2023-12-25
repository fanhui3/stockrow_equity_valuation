import data
import pandas
from statistics import mean
import math


def get_avg_yoy_growth(history):
    """gets average growth from the past few years. function ingests a list of values
    function returns a 1 value

    Args:
        history (List): Past x years of operating performance

    Returns:
        float: average growth rate in 1.xxx%
    """
    growth_history = []

    # calculate the growth between each year. add to the list
    for i in range(0, (len(history) - 1)):
        growth = (history[i] - history[i + 1]) / abs(history[i + 1])
        growth_history.append(growth)

    # get the average growth
    average_growth_rate = 1 + mean(growth_history)
    return average_growth_rate


def get_cagr_growth(history):
    """gets cagr growth from the past few years. function ingests a list of values
    function returns a 1 value

    Args:
        history (List): Past x years of operating performance

    Returns:
        Float: return CAGR growth rate in 1.xxx%
    """
    # calculate CAGR
    try:
        base = history[0] / history[-1]
        power = 1 / (len(history) - 1)
        average_growth_rate = math.pow(base, power)
        return average_growth_rate
    except ValueError:
        print("problem occured. Base year is negative value")
        return 0


def get_min_yoy_growth(history):
    """gets minimum growth rate from the past few years. If it is less than 1, assume no growth

    Args:
        history (list): _Past x years of operating performance

    Returns:
        int: return minimum growth rate in 1.xxx%
    """
    growth_history = []

    # calculate the growth between each year. add to the list
    for i in range(0, (len(history) - 1)):
        growth = (history[i] - history[i + 1]) / abs(history[i + 1])
        growth_history.append(growth)

    # get the minimum growth
    if min(growth_history) >= 0:
        min_growth_rate = 1 + min(growth_history)
    else:
        min_growth_rate = 1

    return min_growth_rate

def growth_history_report(OCF:list = None, net_income: list = None,FCF:list = None, dividends:list = None):
    valuation = ["OCF", "net_income", "FCF", "dividends"]
    histories = {}
    for val in valuation:
        if val == "OCF":
            histories[val] = OCF if OCF else None
        elif val == "net_income":
            histories[val] = net_income if net_income else None
        elif val == "FCF":
            histories[val] = FCF if FCF else None
        elif val == "dividends":
            histories[val] = dividends if dividends else None

    for key, history in histories.items():
        try:
            print(f"history: {key}")
            print(f"Average growth rate: {(get_avg_yoy_growth(history)-1)*100:.2f}%")
            print(f"CAGR growth rate: {(get_cagr_growth(history)-1)*100:.2f}%")
            print("\n")
        except ZeroDivisionError:
            pass


def get_future_values(history, average_growth_rate, average_growth_rate_cap=1.15):
    """get list of future values via the growth rates function ingests a list of past values,
    average growth rate, and capped average growth rate function returns a list of 10 future value

    Args:
        history (list): past performance. Only the latest is taken to calculate
        average_growth_rate (float): growth rate of the method you use
        average_growth_rate_cap (float, optional): max growth from year 4-10, in case the past growth
        rate is too aggressive. Defaults to 1.15.

    Returns:
        list: the projected amount from year 1-10 in the future
    """
    future_value = []
    start_value = history[0]
    for i in range(1, 11):
        # for year 1 - 3, grow by average growth rate
        if i <= 3:
            value = start_value * average_growth_rate
            future_value.append(value)
            start_value = value
        # for year 4-10, grow by cap growth rate
        elif i > 3:
            value = start_value * average_growth_rate_cap
            future_value.append(value)
            start_value = value
    return future_value


def get_present_values_per_share(future_value, wacc=1.1, no_of_shares=100000000):
    """converts future values into present value and calculate value per share function

    Args:
        future_value (list): projected future cashflow form year 1-10
        wacc (float, optional): WACC. get from metrics module. Defaults to 1.1.
        no_of_shares (int, optional): numbers of share. get from metrics module. Defaults to 100000000.

    Returns:
        float: value per share
    """
    present_value = 0

    for i in range(0, len(future_value)):
        value = future_value[i] / pow(wacc, (i + 1))
        present_value += value

    # calculate present value per share
    fair_value = present_value / no_of_shares

    return fair_value


def get_ave_yoy_growth_DCF_value(
    history, cap_growth=1.15, wacc=1.1, no_of_shares=100000000
):
    """stringing together the past functions to get the final present value using the ave growth
    method

    Args:
        history (list): _Past x years of operating performance
        cap_growth (float, optional):max growth from year 4-10, in case the past growth
        rate is too aggressive. Defaults to 1.15.
        wacc (float, optional): WACC. get from metrics module. Defaults to 1.1.
        no_of_shares (int, optional): numbers of share. get from metrics module. Defaults to
        100000000.

    Returns:
        float: value per share
    """
    # find average growth rate
    average_growth_rate = get_avg_yoy_growth(history)

    # for year 4-10, if average growth in year 1-3 is more than 15%, cap it at 15%
    if average_growth_rate > cap_growth:
        average_growth_rate_cap = cap_growth
    else:
        average_growth_rate_cap = average_growth_rate

    # get next 10 years of future value
    future_value = get_future_values(
        history, average_growth_rate, average_growth_rate_cap
    )

    # bring each future value back to present and get per share value
    fair_value = get_present_values_per_share(future_value, wacc, no_of_shares)

    return fair_value


def get_cagr_growth_DCF_value(
    history, cap_growth=1.15, wacc=1.1, no_of_shares=100000000
):
    """stringing together the past functions to get the final present value using the CAGR growth
    method

    Args:
        history (list): _Past x years of operating performance
        cap_growth (float, optional):max growth from year 4-10, in case the past growth
        rate is too aggressive. Defaults to 1.15.
        wacc (float, optional): WACC. get from metrics module. Defaults to 1.1.
        no_of_shares (int, optional): numbers of share. get from metrics module. Defaults to
        100000000.

    Returns:
        float: value per share
    """

    average_growth_rate = get_cagr_growth(history)

    # for year 4-10, if average growth in year 1-3 is more than 15%, cap it at 15%
    if average_growth_rate > cap_growth:
        average_growth_rate_cap = cap_growth
    else:
        average_growth_rate_cap = average_growth_rate

    # get next 10 years of future value
    future_value = get_future_values(
        history, average_growth_rate, average_growth_rate_cap
    )

    # bring each future value back to present and get per share value
    fair_value = get_present_values_per_share(future_value, wacc, no_of_shares)

    return fair_value


def perpetual_dividend_growth_valuation(history, wacc=1.1):
    """get peputual dividend growth valuation

    Args:
        history (list): _Past x years of operating performance
        wacc (float, optional): WACC. get from metrics module. Defaults to 1.1.

    Returns:
        float: valuation/share
    """
    min_growth_rate = get_min_yoy_growth(history)

    # bring to current year and then project for next year. assuming we missed this year's payment
    next_payment = history[0] * min_growth_rate * min_growth_rate

    # apply formula
    valuation = next_payment / (wacc - min_growth_rate)
    return valuation


def perpetual_FCF_growth_valuation(history, wacc=1.1, no_of_shares=100000000):
    """get peputual FCF growth valuation pershare

    Args:
        history (list): _Past x years of operating performance
        wacc (float, optional): WACC. get from metrics module. Defaults to 1.1.
        no_of_shares (int, optional): numbers of share. get from metrics module. Defaults to
        100000000.

    Returns:
        float: valuation/share
    """
    min_growth_rate = get_min_yoy_growth(history)

    # bring to current year and then project for next year. assuming we missed this year's payment
    next_payment = history[0] * min_growth_rate * min_growth_rate

    # apply formula
    valuation = next_payment / (wacc - min_growth_rate)
    valuation = valuation / no_of_shares
    return valuation


if __name__ == "__main__":
    df = data.get_data()
    OCF_History = list(df.iloc[:4]["Operating_Cash_Flow"])
    # OCF_CAGR_GROWTH = get_cagr_growth_DCF_value(
    #     history=OCF_History, cap_growth=1.15, wacc=1.07, no_of_shares=10000
    # )
    print(OCF_History[-1])
