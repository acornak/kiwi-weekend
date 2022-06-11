"""
RegioJet search engine
"""
import argparse

from scraper.regiojet import RegiojetScraper
from scraper.flixbus import FlixbusScraper

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("origin", type=str)
parser.add_argument("destination", type=str)
parser.add_argument("departure_date", type=str)
parser.add_argument("currency", nargs='?', type=str)
parser.add_argument("vehicle_type", nargs='?', type=str)

parsed_args = parser.parse_args()

# Initialize class
regiojetScraper = RegiojetScraper(
    parsed_args.origin,
    parsed_args.destination,
    parsed_args.departure_date,
    parsed_args.currency,
    parsed_args.vehicle_type,
)

flixbusScraper = FlixbusScraper(
    parsed_args.origin,
    parsed_args.destination,
    parsed_args.departure_date,
    parsed_args.currency,
    parsed_args.vehicle_type,
)

# regiojet_results = regiojetScraper.handler()
# flixbus_results = flixbusScraper.handler()

print(regiojetScraper.handler())
# print(flixbus_results)
