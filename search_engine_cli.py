"""
RegioJet search engine cli
"""
import argparse
import json
from scraper.search_engine import call_search_engine

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("origin", type=str)
parser.add_argument("destination", type=str)
parser.add_argument("departure_date", type=str)

parsed_args = parser.parse_args()


if __name__ == "__main__":
    result = call_search_engine(parsed_args.origin, parsed_args.destination, parsed_args.departure_date)
    print(json.dumps(result, indent=4))
