from flask import Flask
from kafka import KafkaConsumer
import grpc
import locations_pb2
import persons_pb2
import locations_pb2_grpc
import persons_pb2_grpc
import logging
import json

from app import db
from app.config import config_by_name

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("kafka-person-location-consumers-services")

app = Flask(__name__)
app.config.from_object(config_by_name["prod"])
db.init_app(app)


TOPIC_NAME = 'udaconnect'


def create_person(person):
    channel = grpc.insecure_channel("localhost:5002")
    person_stub = persons_pb2_grpc.PersonServiceStub(channel)

    persons = persons_pb2.PersonsMessage(
        first_name=person["first_name"],
        last_name=person["last_name"],
        company_name=person["company_name"]
    )

    person_stub.Create(persons)


def create_location(location):
    channel = grpc.insecure_channel("localhost:5002")
    location_stub = locations_pb2_grpc.LocationServiceStub(channel)

    locations = locations_pb2.LocationsMessage(
        person_id=location["person_id"],
        creation_time=location["creation_time"],
        latitude=location["latitude"],
        longitude=location["longitude"]
    )

    location_stub.Create(locations)


consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[
                         'kafka.default.svc.cluster.local:9092'])

for message in consumer:
    d_msg = json.loads((message.value.decode('utf-8')))

    if 'first_name' in d_msg:
        create_person(d_msg)
    elif 'latitude' in d_msg or 'longitude' in d_msg:
        create_location(d_msg)
    else:
        logger.warning(
            "Failed to process the message")
