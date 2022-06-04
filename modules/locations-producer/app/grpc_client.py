import grpc
import locations_pb2
import locations_pb2_grpc

import time

# Assume sending of coordinates personal device
print("Sending coordinates")

channel = grpc.insecure_channel("localhost:9093")
stub = locations_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
first_location = locations_pb2.Location(
    person_id="11",
    latitude=47.0707,
    longitude=15.4395
)

print("Send coordinate 1 .. ")

stub.Create(first_location)

second_location = locations_pb2.Location(
    person_id="12",
    latitude=37.7749,
    longitude=122.4194
)

print("Send coordinate 2 ..")

stub.Create(first_location)

print("Coordinates sent ..")
