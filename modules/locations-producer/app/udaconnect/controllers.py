from app.udaconnect.models.location import Location
from app.udaconnect.services import LocationService
from flask_restx import Namespace, Resource
from flask import request


DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Persons Connections via geolocation.")  # noqa


# TODO: This needs better exception handling


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    def post(self) -> Location:
        payload = {
            'person_id': request.args.get('person_id'),
            'creation_time': request.args.get('creation_time'),
            'latitude': request.args.get('latitude'),
            'longitude': request.args.get('longitude')
        }

        location: Location = LocationService.create(payload)

        return location

    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
