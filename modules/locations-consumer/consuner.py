from __future__ import annotations
from typing import Dict

import json
from kafka import KafkaConsumer
import psycopg2
import logging

from app.udaconnect.database import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

TOPIC_NAME = "location"
messages = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[
    "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"])


def add_location(location: Dict):
    session = psycopg2.connect(
        dbname=DB_NAME,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST
    )

    cursor = session.cursor()
    cursor.execute(
        "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_POINT({}, {}));".format(
            int(location["person_id"]), float(
                location["latitude"]), float(location["longitude"])
        )
    )

    session.commit()
    cursor.close()
    session.close()

    logging.info("Location added to DB")
    return location


def consume_message():
    for message in messages:
        location = json.loads(message.value.decode("utf-8"))
        add_location(location)


logging.basicConfig()
consume_message()
