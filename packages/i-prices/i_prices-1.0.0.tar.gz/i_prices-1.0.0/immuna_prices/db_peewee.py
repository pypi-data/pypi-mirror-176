import logging
from . import cmc, utils
from datetime import datetime
import json
import os
import pandas
from peewee import *
from dotenv import load_dotenv

load_dotenv('.env.local')

db = PostgresqlDatabase(os.getenv('DB_NAME'), user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'))

logging.info('Starting db_peewee.py on {}'.format(os.getenv('DB_HOST')))


class BaseModel(Model):
    class Meta:
        database = db


class AssetPricesCmc(BaseModel):

    class Meta:
        indexes = (
            (('symbol', 'timestamp', 'cmc_id'), True),
        )
    cmc_id = IntegerField()

    Date = CharField()
    Open = FloatField()
    High = FloatField()
    Low = FloatField()
    Close = FloatField()
    Volume = BigIntegerField()
    Market_cap = BigIntegerField()

    symbol = CharField()
    timestamp = DateTimeField()

    addresses = TextField()
    platforms = TextField()

    class Meta:
        primary_key = CompositeKey('timestamp', 'Date', 'symbol')


class AssetInfoCmc(BaseModel):
    cmc_id = IntegerField(unique=True)

    symbol = CharField()
    name = CharField()
    slug = CharField()
    logo = CharField()
    slug = CharField()
    notice = CharField()
    subreddit = CharField()
    category = CharField()
    description = TextField()

    date_added = CharField()
    tags = TextField()
    tag_names = TextField()
    tag_groups = TextField()
    urls = TextField()
    contract_address = TextField()
    platform = TextField()

    last_prices_update = DateTimeField()

    class Meta:
        indexes = (
            (('symbol', 'cmc_id', 'contract_address'), True),
        )


def upsert_currency_info(currency_info_raw):
    currency_info = currency_info_raw[list(currency_info_raw.keys())[0]]
    with db:
        id = (AssetInfoCmc.insert(
            cmc_id=currency_info['id'],
            symbol=currency_info['symbol'],
            name=currency_info['name'],
            slug=currency_info['slug'],
            logo=currency_info['logo'],
            notice=currency_info['notice'],
            subreddit=currency_info['subreddit'],
            category=currency_info['category'],
            description=currency_info['description'],
            date_added=currency_info['date_added'],
            tags=json.dumps(currency_info['tags']),
            tag_names=json.dumps(currency_info['tag-names']),
            tag_groups=json.dumps(currency_info['tag-groups']),
            urls=json.dumps(currency_info['urls']),
            contract_address=list(
                map(lambda x: x["contract_address"], currency_info["contract_address"])),
            platform=list(
                map(lambda x: x["platform"]["name"], currency_info["contract_address"])),
            last_prices_update=datetime.now()

        ).on_conflict_ignore(

        ).execute())
        result = AssetInfoCmc.get(AssetInfoCmc.id == id)
    return result


def check_symbol(symbol):
    with db:
        symbol_info = AssetInfoCmc.select().where(AssetInfoCmc.symbol == symbol)

    return symbol_info[0] if len(symbol_info) > 0 else None


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
            "timestamp": utils.get_date_from_string(row[0]),
            "symbol": db_info.symbol,
            "platforms": db_info.platform,
            "addresses": db_info.contract_address,

        }
        data_to_push.append(row_data)
    print('Pushing to db')
    with db:
        AssetPricesCmc.insert_many(data_to_push).execute()

    print("Added data for ", db_info.name,
          db_info.symbol, " to db")
    # we update the last update date to the last date in the data
    change_info_last_update(db_info, rows[1][0])


def change_info_last_update(db_info, date_string):
    db_info.last_prices_update = utils.get_date_from_string(date_string)
    with db:
        db_info.save()


def get_db_prices(symbol, start_date, end_date) -> pandas.DataFrame:
    with db:
        prices = AssetPricesCmc.select().where(
            AssetPricesCmc.symbol == symbol,
            AssetPricesCmc.timestamp >= start_date,
            AssetPricesCmc.timestamp <= end_date
        )
    return pandas.DataFrame(list(prices.dicts()))


def add_info(symbol):
    cmc_info = cmc.get_cmc_crypto_by_symbol(symbol)
    db_info = upsert_currency_info(cmc_info)
    return db_info


with db:
    db.create_tables([AssetInfoCmc, AssetPricesCmc])
