"""
Scraper itself
"""
import requests

from datetime import datetime
import utils


class FlixbusScraper:
    """
    Regiojet Scraper class (or requests handler...)
    """
    def __init__(self, origin, destination, departure_date, redis):
        """
        """
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.redis = redis

    def get_locations(self):
        """
        Method to get locations from API
        """
        redis_key = "cornak:locations:flixbus"

        locations = utils.retrieve_dict(self.redis, redis_key)

        if not locations:
            locations_url = "https://map-search.cms.flix.tech/cities/_search"
            locations_list = requests.get(locations_url).json()["hits"]["hits"]

            locations = {}

            for hit in locations_list:
                for id, dict in hit["_source"]["connections"].items():
                    print(id)
                    self.__append_location(id, dict["slug"].capitalize())

            utils.store_dict(self.redis, redis_key, locations)

        return locations

    def check_valid_values(self, locations):
        """
        Method to validate all inputs
        """
        if self.origin not in locations:
            print("origin not found in database")
            return False

        if self.destination not in locations:
            print("destination not found in database")
            return False

        try:
            datetime.strptime(self.departure_date, "%Y-%m-%d")
        except ValueError:
            print("date is not valid")
            return False

        return True

    def get_routes(self, locations):
        """
        Route search
        """
        redis_key = f"cornak:routes:{self.origin}{self.destination}{self.departure_date}"
        
        found_routes = utils.retrieve_dict(self.redis, redis_key)

        if not found_routes:
            routes_url = "https://global.api.flixbus.com/search/service/v2/search?from_city_id=9638&to_city_id=1374&departure_date=12.06.2022&products=%7B%22adult%22%3A1%7D&currency=CZK&locale=cs&search_by=cities&include_after_midnight_rides=1&min_price=1"
            routes_url = "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple"
            params = {
                "tariffs": "REGULAR",
                "toLocationType": "CITY",
                "toLocationId": locations[self.destination],
                "fromLocationType": "CITY",
                "fromLocationId": locations[self.origin],
                "departureDate": self.departure_date
            }
            found_routes = requests.get(routes_url, params).json()

            utils.store_dict(self.redis, redis_key, found_routes)
         
        return found_routes

    def transform_result(self, found_routes):
        """
        Transform response to result
        """
        results = []

        for route in found_routes["routes"]:
            results.append(
                {
                    "departure_datetime": utils.transform_date(route["departureTime"]),
                    "arrival_datetime": utils.transform_date(route["arrivalTime"]),
                    "source": self.origin.capitalize(),
                    "destination": self.destination.capitalize(),
                    "fare":  {
                        "amount": route["priceFrom"],
                        "currency": "EUR"
                    },
                    "type": " ".join(route["vehicleTypes"]).lower(),
                    "source_id": route["departureStationId"],
                    "destination_id": route["arrivalStationId"],
                    "free_seats": route["freeSeatsCount"],
                    "carrier": "REGIOJET"
                }
            )
        
        return results
