"""
Utils
"""
import json

from typing import Optional
from redis import Redis
from datetime import datetime


def transform_date(date: str) -> str:
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
