from concurrent import futures
import grpc
import locations_pb2
import locations_pb2_grpc
from locations_pb2_grpc import LocationServiceServicer
import json
from kafka import KafkaProducer
import time


class LocationServicer(locations_pb2_grpc.LocationServiceServicer):
    def Create(self, request):

        request = {
            'person_id': request.person_id,
            'longitude': request.longitude,
            'latitude': request.latitude
        }

        print('Processing request mesage' + request)
        producer.send(TOPIC_NAME, json.dumps(
            request, indent=2).encode('utf-8'))

        return locations_pb2.Location(**request)


time.sleep(15)

TOPIC_NAME = "location-processing"
KAFKA_SERVER = 'kafka-0.default.svc.cluster.local:9092'

print("Connecting to Kafka server: " + KAFKA_SERVER)
print("Sending message Kafka topic: " + TOPIC_NAME)

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
locations_pb2_grpc.add_LocationServiceServicer_to_server(
    LocationServiceServicer(), server)

print('gRPC Server starting on port 5000')
server.add_insecure_port('[::]:5000')
server.start()
server.wait_for_termination()
