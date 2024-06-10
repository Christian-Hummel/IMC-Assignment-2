from flask import jsonify

from flask_restx import Namespace, Resource, fields, abort

from ..model.agency import Agency
from ..database import Country,Activity, db

country_ns = Namespace("country", description="Country related operations")

country_input_model = country_ns.model("CountryModel", {
    "name": fields.String(required=True,
                          help="name of a country. e.g. Switzerland"),

})

country_output_model = country_ns.model("CountryOutputModel", {
    "country_id" : fields.Integer(required=False,
                                  help="unique identifier of a country"),
    "name": fields.String(required=True,
                          help="name of a country. e.g. Switzerland")
})


activity_input_model = country_ns.model("ActivityInputModel", {
    "name": fields.String(required=True,
                          help="name of an activity e.g. Wakeboarding"),
    "price": fields.Integer(required=True,
                            help="price of an activity")
})

activity_output_model = country_ns.model("ActivityOutputModel",{
    "activity_id": fields.Integer(required=True,
                                  help="the unique identifier of an activity"),
    "name": fields.String(required=True,
                          help="name of an activity e.g. Wakeboarding"),
    "price": fields.Integer(required=True,
                            help="price of an activity")
})

# Country

@country_ns.route("/")
class CountryAPI(Resource):

    @country_ns.doc(country_input_model,description="Add a country to the database")
    @country_ns.expect(country_input_model,validate=True)
    @country_ns.marshal_with(country_output_model, envelope="country")
    def post(self):
        # Create new Country object
        new_country = Country(country_id=id(self), name=country_ns.payload["name"])
        # Check for duplicates
        same_country = db.session.query(Country).filter_by(name=new_country.name).first()

        if same_country: # throw an error if the same country is already in the database
            return abort(400, message="This country is already registered")

        Agency.get_instance().add_country(new_country)

        return new_country

    @country_ns.doc(country_output_model, description="Get information about all countries")
    @country_ns.marshal_list_with(country_output_model, envelope="countries")
    def get(self):


        countries = Agency.get_instance().get_all_countries()

        if countries:
            return countries
        elif not countries:
            return jsonify("There are no countries registered in the database")


@country_ns.route("/<int:country_id>")
class CountryInfo(Resource):

    @country_ns.doc(description="Get information about a single country")
    def get(self,country_id):

        targeted_country = Agency.get_instance().get_country_by_id(country_id)

        if targeted_country:
            return targeted_country
        else:
            return abort(400, message="country not found")


# Activity

@country_ns.route("/<int:country_id>/activity")
class ActivityAPI(Resource):


    @country_ns.doc(activity_input_model,description="Add an activity to a specific country")
    @country_ns.expect(activity_input_model,validate=True)
    @country_ns.marshal_with(activity_output_model,envelope="activity")
    def post(self,country_id):

        new_activity = Activity(activity_id=id(self),
                                name=country_ns.payload["name"],
                                price=country_ns.payload["price"])



        if new_activity.price <= 0:
            return abort(400,message="Please enter a valid price for this activity")

        Agency.get_instance().add_activity(new_activity, country_id)

        return new_activity


@country_ns.route("/<int:country_id>/activity/update")
class ActivityUpdate(Resource):

    @country_ns.doc(activity_output_model, description="Update an activity")
    @country_ns.expect(activity_output_model,validate=True)
    @country_ns.marshal_with(activity_output_model,envelope="activity")
    def post(self,country_id):


        activity_id = country_ns.payload["activity_id"]
        # check if this activity exists
        targeted_activity = db.session.query(Activity).filter_by(activity_id=activity_id).one_or_none()
        targeted_country = db.session.query(Country).filter_by(country_id=country_id).one_or_none()

        if not targeted_activity: # throw an error if it is not registered
            return abort(400, message="Activity not found")

        if not targeted_country: # throw an error if country is not registered
            return abort(400, message="Country not found")

        elif targeted_activity:
            activity_id = targeted_activity.activity_id
            updated_activity = Activity(activity_id=activity_id,
                                        name=country_ns.payload["name"],
                                        price=country_ns.payload["price"])

            if updated_activity.name not in ["string",targeted_activity.name] or updated_activity.price != targeted_activity.price:
                Agency.get_instance().update_activity(updated_activity, country_id)
                return updated_activity
            else:
                return abort(400, message="Please insert values to be updated")


