import json
import logging
from typing import Dict, List
from datetime import datetime, timedelta

from app import db
from app.udaconnect.models import Person, Connection, Location
from sqlalchemy.sql import text

from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("persons-connection-api")

TOPIC_NAME = "udaconnect"
KAFKA_SERVER = "kafka.default.svc.cluster.local:9092"

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
print("Init Kafka Producer")


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        """"
        Processing person creation data with Kafka
        """
        new_person = json.dumps(person).encode()
        producer.send(TOPIC_NAME, new_person)
        producer.flush()

        return "Request Accept"

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()


class ConnectionService:
    @staticmethod
    def find_connection(
        person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Find connections with a given distance and a date range
        """
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date
                 ).filter(Location.creation_time >= start_date).all()

        person_map: Dict[str, Person] = {
            person.id: person for person in PersonService.retrieve_all()
        }

        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        raw_query = text(
            """
            SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
            FROM    location
            WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
            AND     person_id != :person_id
            AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
            AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
            """
        )

        result: List[Connection] = []
        for line in tuple(data):
            for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
            ) in db.engine.execute(raw_query, **line):
                location = Location(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=exposed_time,
                )

                location.set_wkt_with_coords(exposed_lat, exposed_long)

                result.append(
                    Connection(
                        person=person_map[exposed_person_id], location=location,)
                )

        return result
