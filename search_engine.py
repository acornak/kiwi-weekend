"""
RegioJet search engine
"""
import argparse

from redis import Redis

from scraper.scrapers import Scraper
from scraper.regiojet import RegiojetScraper

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("origin", type=str)
parser.add_argument("destination", type=str)
parser.add_argument("departure_date", type=str)
parser.add_argument("currency", nargs='?', type=str)

parsed_args = parser.parse_args()

# Redis setup
host = "redis.pythonweekend.skypicker.com"
password = "a9c7a440-cef7-4de1-92ce-e7f922511c0b"
redis = Redis(host=f"{host}", port=6379, db=0, password=f"{password}", decode_responses=True)

# Initialize carriers
list_of_carriers = ["REGIOJET"]
result = []

for carrier in list_of_carriers:
    scraper = Scraper(
        parsed_args.origin,
        parsed_args.destination,
        parsed_args.currency,
        parsed_args.departure_date,
        carrier,
        redis
    )
    result.append(scraper.handler())

print(result)
