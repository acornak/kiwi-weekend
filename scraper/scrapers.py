"""

"""
from redis import Redis

from scraper.regiojet import RegiojetScraper
from scraper.flixbus import FlixbusScraper

SCRAPERS = {
    "REGIOJET": RegiojetScraper,
    "FLIXBUS": FlixbusScraper
}

class Scraper:
    """
    Scraper class
    """
    def __init__(self, origin: str, destination: str, departure_date: str, carrier: str, sql_session, redis = Redis):
        """
        Initialization
        """
        self.origin = origin.lower()
        self.destination = destination.lower()
        self.departure_date = departure_date
        self.carrier = carrier
        self.redis = redis
        self.sql_session = sql_session
        self.engine = SCRAPERS[carrier]
    
    def handler(self) -> list:
        """
        Orchestration for scraper class
        """
        engine = self.engine(
            self.origin, 
            self.destination, 
            self.departure_date, 
            self.sql_session,
            self.redis
        )

        status, locations = engine.get_locations()

        # TODO: move validation here
        valid_values = engine.check_valid_values(locations)

        # TODO:
        if not valid_values:
            return (400, "invalid input parameters")
        
        status, found_routes = engine.get_routes(locations)
        
        if not status:
            return (400, found_routes)

        status, transformed_routes = engine.transform_result(found_routes)

        if not status:
            return (400, transformed_routes)

        if not engine.append_routes_to_database(transformed_routes):
            print("database update was not successful")

        return (200, transformed_routes)
        
        