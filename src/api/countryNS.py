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

activityID_model = country_ns.model("ActivityDeleteModel", {
    "activity_id": fields.Integer(required=True,
                                 help="unique identifier of activity to be removed from this country")
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
            return abort(400,message="There are no countries registered in the agency")


@country_ns.route("/<int:country_id>")
class CountryInfo(Resource):

    @country_ns.doc(description="Get information about a single country")
    def get(self,country_id):

        targeted_country = Agency.get_instance().get_country_by_id(country_id)

        if targeted_country:
            return targeted_country
        else:
            return abort(400, message="country not found")

@country_ns.route("/<int:country_id>/stats")
class CountryStats(Resource):


    @country_ns.doc(description="Get detailed Information about a Country")
    def get(self,country_id):

        country = db.session.query(Country).filter_by(country_id=country_id).one_or_none()

        if not country:
            return abort(400, message="Country not found")

        stats = Agency.get_instance().get_country_stats(country)

        if stats:
            return stats
        if not stats:
            return abort(400, message="This country has not been visited by a customer yet")

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




@country_ns.route("/<int:country_id>/activity/<int:activity_id>")
class ActivityInfo(Resource):

    @country_ns.doc(description="Get information about an activity")
    @country_ns.marshal_with(activity_output_model, envelope="activity")
    def get(self, country_id, activity_id):



        country = db.session.query(Country).filter_by(country_id=country_id).one_or_none()
        activity = db.session.query(Activity).filter_by(activity_id=activity_id).one_or_none()

        if not activity:
            return abort(400, message="Activity not found")

        if not country:
            return abort(400, message="Country not found")

        targeted_activity = Agency.get_instance().get_activity_by_id(country,activity)

        if targeted_activity:
            return activity

        elif not targeted_activity:
            return abort(400, message=f"This activity is not registered for {country.name}")


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


@country_ns.route("/<int:country_id>/activity/delete")
class ActivityDelete(Resource):

    @country_ns.doc(activityID_model,description="Delete an Activity")
    @country_ns.expect(activityID_model, validate=True)
    def delete(self,country_id):

        activity_id = country_ns.payload["activity_id"]
        # check if activity is registered
        r_activity = db.session.query(Activity).filter_by(activity_id=activity_id).one_or_none()
        # check if country is registered
        country = db.session.query(Country).filter_by(country_id=country_id).one_or_none()

        if not r_activity:
            return abort(400, message="Activity not found")

        if not country:
            return abort(400, message="Country not found")

        updated_country = Agency.get_instance().remove_activity(country,r_activity)

        if updated_country:
            return jsonify(f"Activity {r_activity.name} has been removed from {updated_country.name}")

        elif not updated_country:
            return abort(400, message="This activity does not belong to the specified country")