"""
Journey repository script
"""
from sqlalchemy.orm.session import Session

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
    
    def get_journey(self):
        """
        Get journey from the database
        """
        
        
        pass

    def set_journey(self, route: dict) -> bool:
        """
        Insert journey into the database
        """
        journey = Journey(
            source=route["source"], 
            destination=route["destination"],
            departure_datetime=route["departure_datetime"],
            arrival_datetime=route["arrival_datetime"],
            carrier=route["carrier"], 
            vehicle_type=route["type"],
            price=float(route["fare"]["amount"]),
            currency=route["fare"]["currency"]
        )

        with self.sql_session as session:
            session.add(journey)
            session.commit()

        return True
