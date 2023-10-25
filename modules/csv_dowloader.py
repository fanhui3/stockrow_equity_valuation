from . import stockrow_scraper_api
from . import file_mover
import time

ticker = "hsy"


def download_csv(ticker):
    stockrow_scraper_api.get_stockrow_data(ticker)
    time.sleep(3)
    file_mover.format_copy_file()
