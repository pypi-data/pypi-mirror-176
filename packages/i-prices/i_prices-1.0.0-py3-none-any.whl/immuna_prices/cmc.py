from .utils import get_cmc_data, get_url_data


def get_trending_cryptos_json():
    api_url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/trending/latest'

    return get_cmc_data(api_url)

def get_cmc_crypto_by_symbol(symbol):
    url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/info?symbol={}".format(symbol)
    
    return get_cmc_data(url)


def get_cmc_crypto_by_symbols(symbols):
    url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/info?symbol={}".format(",".join(symbols))
    
    return get_cmc_data(url)

def get_cmc_crypto_by_address(address):
    url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/info?address={}".format(address)
    
    return get_cmc_data(url)