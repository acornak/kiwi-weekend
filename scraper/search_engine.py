"""
RegioJet search engine
"""
from redis import Redis

from scraper.scrapers import Scraper
from database.init_database import initialize_database

def call_search_engine(origin: str, destination: str, departure_date: str) -> str:
    """
    Function to call search
    """
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
            origin.lower(),
            destination.lower(),
            departure_date,
            carrier,
            sql_session,
            redis_session
        )
        status, message = scraper.handler()

        # todo
        if status == 200:
            result += message
        else:
            print(f"{carrier} search was not successful: {message}")

    return result
