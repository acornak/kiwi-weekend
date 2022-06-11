"""
Scraper itself
"""
import sys
import requests
import json

from datetime import datetime
import utils


class RegiojetScraper:
    """
    Regiojet Scraper class (or requests handler...)
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
        locations_url = "https://brn-ybus-pubapi.sa.cz/restapi/consts/locations"
        locations_list = requests.get(locations_url).json()

        for country in locations_list:
            for city in country["cities"]:
                self.locations[city["name"].lower()] = str(city["id"])

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
                    "fare":  utils.handle_currencies(self.currency, route["priceFrom"]),
                    "type": " ".join(route["vehicleTypes"]).lower(),
                    "source_id": route["departureStationId"],
                    "destination_id": route["arrivalStationId"],
                    "free_seats": route["freeSeatsCount"],
                    "carrier": "REGIOJET"
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


