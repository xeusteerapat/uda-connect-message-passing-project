import grpc
import locations_pb2
import persons_pb2
import locations_pb2_grpc
import persons_pb2_grpc

print("Sending sample payload")

channel = grpc.insecure_channel("localhost:5002")
location_stub = locations_pb2_grpc.LocationServiceStub(channel)
person_stub = persons_pb2_grpc.PersonServiceStub(channel)

# Update this with desired payload
locations = locations_pb2.LocationsMessage(
    person_id=99,
    creation_time='18:00 hrs GMT+7',
    latitude='13.756331',
    longitude='100.501762'
)

persons = persons_pb2.PersonsMessage(
    id=1,
    first_name='Teerapat',
    last_name='Prommarak',
    company_name='MOHARA'
)


response = location_stub.Create(locations)
response = person_stub.Create(persons)
