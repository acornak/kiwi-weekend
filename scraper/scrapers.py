"""

"""
import sys
import requests
import json

from typing import Optional
from redis import Redis
from datetime import datetime

from scraper.regiojet import RegiojetScraper
from scraper.flixbus import FlixbusScraper

SCRAPERS = {
    "REGIOJET": RegiojetScraper,
    "FLIXBUS": FlixbusScraper
}

class Scraper:
    """
    
    """
    REDIS_HOST = ""
    REDIS_PASSWORD = ""

    def __init__(self, origin, destination, departure_date, currency, carrier, redis = Redis):
        """

        """
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.currency = currency
        # compostion
        self.engine = SCRAPERS[carrier]
        self.redis = redis
    
    def handler(self):
        """
        Orchestration for scraper class
        """
        engine = self.engine(
            self.origin, 
            self.destination, 
            self.departure_date, 
            self.currency, 
            self.redis
        )

        locations = engine.get_locations()
        valid_values = engine.check_valid_values(locations)

        if not valid_values:
            print(f"{self.carrier} did not found any matching routes. Check arguments and try again")
            return {}
        
        found_routes = engine.get_routes(locations)

        return engine.transform_result(found_routes)
        
        