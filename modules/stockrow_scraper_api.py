import webbrowser
import time
import os

# get the file path of one folder up
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APIS = [
    # "https://stockrow.com/api/companies/{}/financials.xlsx?dimension=A&section=Income%20Statement&sort=desc",
    # "https://stockrow.com/api/companies/{}/financials.xlsx?dimension=A&section=Balance%20Sheet&sort=desc",
    # "https://stockrow.com/api/companies/{}/financials.xlsx?dimension=A&section=Cash%20Flow&sort=desc",
    # "https://stockrow.com/api/companies/{}/financials.xlsx?dimension=A&section=Metrics&sort=desc",
    # "https://stockrow.com/api/companies/{}/financials.xlsx?dimension=A&section=Growth&sort=desc",
    "https://stockrow.com/vector/exports/financials/{}?direction=desc"
]


def go_to_site(site_url: str, browser_location: str, stock: str):
    """This function open up the stockrow financial api page in annual format and download the cvs

    Args:
        stock (_str_): the api url for each buttons
        stock (_str_): ticker symbol listed on thy nyse or nasdaq
        browser_location (_str_): location where you keep your brower exe
    """
    url = site_url.format(stock)
    webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(browser_location))
    webbrowser.get("chrome").open(url)


def get_stockrow_data(stock):
    """main function of this package. This functions will look for the chrome browser on the
    computer defined in the txt file, then use it to access the 5 api sites defined in the list
    of API, fill the URL with the ticker symbol and download the xslx.

    Args:
        stock (str): the stocks you want
    """
    stock = stock.upper()
    brower_path = open(f"{file_path}/browser_location.txt", "r").readline()
    for api in APIS:
        go_to_site(api, brower_path, stock)
        time.sleep(1)


if __name__ == "__main__":
    ticker = "pins"
    get_stockrow_data(ticker)
