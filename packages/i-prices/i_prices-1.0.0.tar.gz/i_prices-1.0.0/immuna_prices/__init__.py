from concurrent.futures import ThreadPoolExecutor
import logging
import multiprocessing
import sys
import pandas
from .cmc import *
from datetime import datetime
from cryptocmd import CmcScraper
from . import utils, db_peewee
import pytz
utc = pytz.UTC

executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 2)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
)
logging.StreamHandler(stream=sys.stdout)


def get_prices(symbol: str, start_date: str, end_date: str, logs=False) -> pandas.DataFrame:
    """_summary_: Get prices for a given symbol from start_date to end_date
    If no data is found in the database, it will be downloaded from coinmarketcap.com
    If data is found in the database, it will be returned from the database, including addresses and platforms

    Args:
        symbol (str): currency symbol
        start_date (str): start date - ie. 01-01-2018
        end_date (str): end date - ie. 01-02-2019
        logs (bool): show logs 

    Returns:
        pandas.DataFrame: dataframe with prices
    """
    if (logs):
        logging.getLogger().setLevel(logging.DEBUG)

    local_start_date = utc.localize(utils.get_date_from_string(start_date))
    local_end_date = utc.localize(utils.get_date_from_string(end_date))
    logging.debug("Getting prices for {} from {} to {}".format(
        symbol, start_date, end_date))
    try:
        db_info = db_peewee.check_symbol(symbol)

        if (db_info is not None and local_end_date > utc.localize(db_info.last_prices_update)):
            logging.debug("Updating prices for {} because {} > {}".format(
                local_end_date, db_info.last_prices_update))
            executor.submit(update_prices_from,
                            (symbol, db_info.last_prices_update, db_info))
        elif (db_info is not None and local_end_date <= utc.localize(db_info.last_prices_update)):
            # if we got this token in DB and it was last updated before the end date we return it from DB
            logging.debug("Getting prices from DB, because {} <= {}".format(
                local_end_date, db_info.last_prices_update))
            return db_peewee.get_db_prices(symbol, local_start_date, local_end_date)
        elif (db_info is None):
            logging.debug("Adding prices for {}".format(symbol))
            executor.submit(add_prices_from, (symbol))
        # if this is a new token we will just return the data from the scraper
        logging.debug(
            "Getting prices from scraper, and caching them in DB in background")
        scraper = CmcScraper(symbol, utils.get_formatted_date(
            local_start_date), utils.get_formatted_date(local_end_date))
        return scraper.get_dataframe()
    # TODO: figure out how to properly stop threadpool executor
    except KeyboardInterrupt:
        logging.debug("KeyboardInterrupt")
        executor.shutdown(wait=False)
        executor._threads.clear()
        return pandas.DataFrame([])
    except:
        logging.exception("Error getting prices for {}".format(symbol))
        return pandas.DataFrame([])


# we are updating prices from last_prices_update date to today's date
def update_prices_from(symbol, start_date, db_info):
    try:
        str_start = utils.get_formatted_date(start_date)
        str_end = utils.get_formatted_date(utc.localize(datetime.today()))
        logging.debug("Updating prices for {} from {} to {}".format(
            symbol, str_start, str_end))
        scraper = CmcScraper(symbol, str_start, str_end)

        rows = scraper.get_data()[1]
        db_peewee.add_prices(rows, db_info)
    except:
        logging.debug("Error updating prices for {}".format(symbol))


def add_prices_from(symbol):
    try:
        db_info = db_peewee.add_info(symbol)
        scraper = CmcScraper(symbol)
        rows = scraper.get_data()[1]
        db_peewee.add_prices(rows, db_info)
    except:
        logging.debug("Error adding prices for {}".format(symbol))


# def clear_db():
#     db.clear_db()
