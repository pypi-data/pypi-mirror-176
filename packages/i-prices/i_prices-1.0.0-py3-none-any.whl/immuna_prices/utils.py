from datetime import datetime
import logging
from requests import get


def get_url_data(url):
    """
    This method downloads the data of the web page.
    :param url: 'url' of the web page to download
    :return: response object of get request of the 'url'
    """

    try:
        response = get(url)
        return response
    except Exception as e:
        if hasattr(e, "message"):
            logging.info("Error message:{}".format(e.message))
        else:
            logging.info("Error message:{}".format(e))
        raise e


def get_cmc_data(url):
    try:
        json_data = get_url_data(url).json()
        error_code = json_data["status"]["error_code"]
        if error_code == 0:
            return json_data["data"]
        else:
            raise Exception(json_data["status"]["error_message"])
    except Exception as e:
        logging.info("Error fetching cmc data rom url {}".format(url))

        if hasattr(e, "message"):
            logging.info("Error message:{}".format(e.message))
        else:
            logging.info("Error message:{}".format(e))


def get_formatted_date(date) -> str:
    return date.strftime("%d-%m-%Y")


def get_date_from_string(date_string) -> datetime:
    return datetime.strptime(date_string, "%d-%m-%Y")
