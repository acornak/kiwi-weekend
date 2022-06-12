"""
Journey repository script
"""
from sqlalchemy.orm.session import Session
from datetime import datetime

from database.init_database import Journey

class JourneyRepository:
    """
    Journey repository class
    """
    def __init__(self, sql_session: Session, ):
        """
        Initialization of the class
        """
        self.sql_session = sql_session

    def get_all_available_data(self):
        """
        Get the whole table
        """
        with self.sql_session as session:
            journeys = session.query(Journey).all()
            for journey in journeys:
                print(
                    "found journey: "
                    f"{journey.source} - {journey.destination}"
                )
    
    def get_journey(self, origin: str, destination: str, departure_datetime: str) -> list:
        """
        Get journey from the database
        """
        with self.sql_session as session:
            result = session.query(Journey).filter(
                Journey.source == origin,
                Journey.destination == destination,
                # Journey.departure_datetime >= datetime.strptime(departure_datetime, "%Y-%m-%d %H:%M")
            ).all()
        
        return list(result)

    def set_journey(self, route: dict) -> bool:
        """
        Insert journey into the database
        """
        journey = Journey(
            source=route["source"], 
            destination=route["destination"],
            departure_datetime=datetime.strptime(route["departure_datetime"], "%Y-%m-%d %H:%M"),
            arrival_datetime=datetime.strptime(route["arrival_datetime"], "%Y-%m-%d %H:%M"),
            carrier=route["carrier"], 
            vehicle_type=route["type"],
            price=float(route["fare"]["amount"]),
            currency=route["fare"]["currency"],
            #TODO: change format
            createdAt=datetime.now(),
        )

        with self.sql_session as session:
            session.add(journey)
            session.commit()

        return True
