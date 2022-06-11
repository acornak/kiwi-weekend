"""
Utils
"""
import sys
import requests
import json

from typing import Optional
from redis import Redis
from datetime import datetime


def handle_currencies(currency, eur_amount):
        """
        Method to handle all currencies
        """
        currencies_url = "https://api.skypicker.com/rates"
        currencies_rates = requests.get(currencies_url).json()

        currency_result = {}

        # handle no currency
        if not currency:
            currency_result["amount"] = eur_amount
            currency_result["currency"] = "EUR"
            return currency_result

        # check if currency is valid
        if currency.upper() not in currencies_rates:
            sys.exit("invalid currency")

        currency_result["amount"] = round(float(eur_amount) / float(currencies_rates[currency.upper()]), 2)
        currency_result["currency"] = currency.upper()

        return currency_result

def transform_date(date):
        """
        Format date
        :param date: date to transform
        :rtype date: str
        :return: transformed date
        :rtype: str
        """
        return datetime.fromisoformat(date).strftime("%Y-%m-%d %H:%M")

def store_dict(redis: Redis, key: str, value: dict) -> None:
    """
    Store dict to redis
    """
    redis.set(key, json.dumps(value))

def retrieve_dict(redis: Redis, key: str) -> Optional[dict]:
    """
    Retrieve dict from redis
    """
    maybe_value = redis.get(key)

    if maybe_value is None:
        return None

    return json.loads(maybe_value)


