from stockrow_scraper_api import get_stockrow_data
from file_mover import format_copy_file
import time

ticker = "baba"

get_stockrow_data(ticker)
time.sleep(3)
format_copy_file()
