"""
RegioJet search engine
"""
from scraper.scraper import RegiojetScraper
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("origin", type=str)
parser.add_argument("destination", type=str)
parser.add_argument("departure_date", type=str)
parser.add_argument("vehicle_type", nargs='?', type=str)
parser.add_argument("currency", nargs='?', type=str)

parsed_args = parser.parse_args()

# Initialize class
regiojetScraper = RegiojetScraper(
    parsed_args.origin,
    parsed_args.destination,
    parsed_args.departure_date,
    parsed_args.vehicle_type,
    parsed_args.currency
)

print(regiojetScraper.handler())
