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
    Scraper class
    """
    def __init__(self, origin, destination, departure_date, currency, carrier, redis = Redis):
        """
        Initialization
        """
        self.origin = origin.lower()
        self.destination = destination.lower()
        self.departure_date = departure_date
        self.currency = currency
        self.carrier = carrier
        self.redis = redis
        self.engine = SCRAPERS[carrier]
    
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
            return
        
        found_routes = engine.get_routes(locations)

        return engine.transform_result(found_routes)
        
        