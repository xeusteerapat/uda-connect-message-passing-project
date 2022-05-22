from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, fields

from app.udaconnect.models.location import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect - Location API", description="Create location data")  # noqa

location_response = api.model("Location", {
    "id": fields.Integer,
    "person_id": fields.Integer,
    "longitude": fields.String,
    "latitude": fields.String,
    "creation_time": fields.DateTime
})


@api.route("/locations")
class LocationListResources(Resource):
    @accepts(schema=LocationSchema)
    @api.doc(
        description="Create a new location",
        body=location_response,
        responses={
            202: "Location creation accepted",
            500: "Internal Server Error"
        }
    )
    def post(self):
        location: Location = request.get_json()

        LocationService.create(location)

        return {
            "status": "accepted"
        }, 202


@api.route("/locations/<location_id>")
@api.params("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    @api.doc(
        description="Get location by given location_id",
        params={
            "location_id": "location id is required"
        },
        responses={
            404: "Location Not Found",
            500: "Internal Server Error"
        }
    )
    @api.response(200, "Location found", location_response)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
