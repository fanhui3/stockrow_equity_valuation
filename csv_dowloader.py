from modules import stockrow_scraper_api
from modules import file_mover
import time

ticker = "pins"

stockrow_scraper_api.get_stockrow_data(ticker)
time.sleep(3)
file_mover.format_copy_file()
