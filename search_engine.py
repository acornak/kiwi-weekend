"""
RegioJet search engine
"""
import argparse
import json 

from redis import Redis

from scraper.scrapers import Scraper
from database.init_database import initialize_database


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("origin", type=str)
    parser.add_argument("destination", type=str)
    parser.add_argument("departure_date", type=str)

    parsed_args = parser.parse_args()

    # Redis setup
    redis_host = "redis.pythonweekend.skypicker.com"
    redis_password = "a9c7a440-cef7-4de1-92ce-e7f922511c0b"
    redis_session = Redis(host=f"{redis_host}", port=6379, db=0, password=f"{redis_password}", decode_responses=True)

    # SQL setup
    sql_username = "anton_cornak"
    sql_password = "fbebd89d15004255b39be32ff98a3bc9"

    sql_url = (
        f"postgresql://{sql_username}:{sql_password}"
        "@sql.pythonweekend.skypicker.com/pythonweekend"
        f"?application_name={sql_username}_local_dev"
    )

    sql_session = initialize_database(sql_url)

    # Initialize carriers
    list_of_carriers = ["REGIOJET"]
    result = []

    for carrier in list_of_carriers:
        scraper = Scraper(
            parsed_args.origin,
            parsed_args.destination.lower(),
            parsed_args.departure_date,
            carrier,
            sql_session,
            redis_session
        )
        result += scraper.handler()

    #print(json.dumps(result, indent=4))
