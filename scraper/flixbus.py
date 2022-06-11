"""
Flixbus scraper itself
"""
import sys
import requests
import json

from datetime import datetime
import utils

class FlixbusScraper:
    """
    Flixbus scraper class (or requests handler...)
    """
    def __init__(self, origin, destination, departure_date, currency, vehicle_type):
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.vehicle_type = vehicle_type
        self.currency = currency
        self.locations = {}
        self.all_vehicle_types = []
        self.results = []

    def __get_locations(self):
        """
        Method to get locations from API
        """
        locations_url = "https://map-search.cms.flix.tech/cities/_search"
        locations_list = requests.get(locations_url).json()["hits"]["hits"]

        for hit in locations_list:
            for id, dict in hit["_source"]["connections"].items():
                print(id)
                self.__append_location(id, dict["slug"].capitalize())

        
    def __append_location(self, id, name):
        """
        Append location to locations
        """
        if name not in self.locations:
            self.locations[name] = id

    def __check_valid_values(self):
        """
        Method to validate all inputs
        """
        if self.origin not in self.locations:
            sys.exit("origin not in database")

        if self.destination not in self.locations:
            sys.exit("destination not in database")

        try:
            datetime.strptime(self.departure_date, "%Y-%m-%d")
        except ValueError:
            sys.exit("date not valid")
        
    def __get_all_vehicle_types(self):
        """
        Method to get all vehicle types
        """
        pass

    def __transform_result(self, found_routes):
        """
        Transform response to result
        """
        for route in found_routes["routes"]:
            self.results.append(
                {
                    "departure_datetime": utils.transform_date(route["departureTime"]),
                    "arrival_datetime": utils.transform_date(route["arrivalTime"]),
                    "source": self.origin.capitalize(),
                    "destination": self.destination.capitalize(),
                    "fare":  utils.handle_currencies(route["priceFrom"]),
                    "type": " ".join(route["vehicleTypes"]).lower(),
                    "source_id": route["departureStationId"],
                    "destination_id": route["arrivalStationId"],
                    "free_seats": route["freeSeatsCount"],
                    "carrier": "FLIXBUS"
                }
            )

    def handler(self):
        """
        Handler for Regiojet Scraper class
        """

        self.__get_locations()
        self.__check_valid_values()

        routes_url = "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple?tariffs=REGULAR" \
                    f"&toLocationType=CITY&toLocationId={self.locations[self.destination]}" \
                    f"&fromLocationType=CITY&fromLocationId={self.locations[self.origin]}" \
                    f"&departureDate={self.departure_date}"
         
        self.__transform_result(requests.get(routes_url).json())

        return json.dumps(self.results, indent=4)


    routes_url = "https://global.api.flixbus.com/search/service/v2/search?from_city_id=9638&to_city_id=1374&departure_date=12.06.2022&products=%7B%22adult%22%3A1%7D&currency=CZK&locale=cs&search_by=cities&include_after_midnight_rides=1&min_price=1"