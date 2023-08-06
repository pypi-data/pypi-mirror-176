from datetime import datetime
import json
import logging
import os
import pandas

from prisma import Prisma
from . import utils, cmc

prisma = Prisma(datasource={
    'url': os.getenv('IMMUNA_DATABASE_URL')
},)


def wrapper(func):
    def inner(*args, **kwargs):
        if (prisma.is_connected()):
            return func(*args, **kwargs)
        else:
            prisma.connect()
            return func(*args, **kwargs)
    return inner


@wrapper
def upsert_currency_info(currency_info_raw):
    currency_info = currency_info_raw[list(currency_info_raw.keys())[0]]
    data = {
        "cmc_id": currency_info["id"],
        "name": currency_info["name"],
        "symbol": currency_info["symbol"],
        "category": currency_info["category"],
        "description": currency_info["description"],
        "slug": currency_info["slug"],
        "logo": currency_info["logo"],
        "subreddit": currency_info["subreddit"],
        "notice": currency_info["notice"],
        "tags": currency_info["tags"] if ("tags" in currency_info and currency_info["tags"] is not None) else [],
        "tag_names": currency_info["tag-names"] if "tag-names" in currency_info and currency_info["tag-names"] is not None else [],
        "tag_groups": currency_info["tag-groups"] if "tag-groups" in currency_info and currency_info["tag-groups"] is not None else [],
        "urls": json.dumps(currency_info["urls"]),
        "platform": json.dumps(currency_info["platform"]),
        "date_added": currency_info["date_added"],
        "twitter_username": currency_info["twitter_username"],
        "is_hidden": currency_info["is_hidden"],
        "date_launched": currency_info["date_launched"],
        "contract_address": json.dumps(currency_info["contract_address"]),
        "self_reported_circulating_supply": currency_info["self_reported_circulating_supply"],
        "self_reported_market_cap": currency_info["self_reported_market_cap"],

        "known_addresses": list(map(lambda x: x["contract_address"], currency_info["contract_address"])),
        "known_platforms": list(map(lambda x: x["platform"]["name"], currency_info["contract_address"])),
        "known": list(map(lambda x: x["platform"]["name"] + ":" + x["platform"]["coin"]["symbol"] + ":" + x["contract_address"], currency_info["contract_address"])),

        "known_scanners": currency_info["urls"]["explorer"],
        "last_prices_update": datetime.now()
    }
    db_info = prisma.cmcassetinfo.upsert(
        where={"cmc_id": currency_info["id"]}, data={"create": data, "update": data})
    logging.debug("Upsert cmc asset info: {} {} ".format(
        currency_info["name"], currency_info["symbol"]))
    return db_info


@wrapper
def check_symbol(symbol):
    symbol_info = prisma.cmcassetinfo.find_first(where={"symbol": symbol})
    return symbol_info


@wrapper
def add_prices(rows, db_info):
    print('Adding prices for', db_info.symbol)
    print('Rows count:', len(rows))
    data_to_push = []
    for row in rows:
        row_data = {
            "Date": row[0],
            "cmc_id": db_info.cmc_id,
            "Open": row[1],
            "High": row[2],
            "Low": row[3],
            "Close": row[4],
            "Volume": row[5],
            "Market_cap": row[6],
            "source": "coinmarketcap",
            "timestamp": utils.get_date_from_string(row[0]),
            "symbol": db_info.symbol,
            "known": db_info.known,
            "known_addresses": db_info.known_addresses,
            "known_scanners": db_info.known_scanners,
        }
        data_to_push.append(row_data)
    print('Pushing to db')
    prisma.assetprice.create_many(data=data_to_push)
    print("Added data for ", db_info.name,
          db_info.symbol, " to db")
    # we update the last update date to the last date in the data
    change_info_last_update(db_info, rows[1][0])


def change_info_last_update(db_info, date_string):
    prisma.cmcassetinfo.update(where={"id": db_info.id}, data={
                               "last_prices_update": utils.get_date_from_string(date_string)})


@wrapper
def get_db_prices(symbol, start_date, end_date) -> pandas.DataFrame:
    prices = prisma.assetprice.find_many(
        where={"symbol": symbol, "timestamp": {"gte": start_date, "lte": end_date}})
    frame = pandas.DataFrame(prices)
    return frame


def add_info(symbol):
    cmc_info = cmc.get_cmc_crypto_by_symbol(symbol)
    db_info = upsert_currency_info(cmc_info)
    return db_info


@wrapper
def clear_db():
    prisma.cmcassetinfo.delete_many()
    prisma.assetprice.delete_many()
