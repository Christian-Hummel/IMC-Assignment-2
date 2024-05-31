from flask_restx import Namespace, Resource, fields, abort

from ..model.agency import Agency
from ..database import Country, db

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


@country_ns.route("/")
class CountryAPI(Resource):

    @country_ns.doc(country_input_model,description="Add a country to the database")
    @country_ns.expect(country_input_model,validate=True)
    @country_ns.marshal_with(country_output_model, envelope="country")
    def post(self):

        new_country = Country(country_id=id(self), name=country_ns.payload["name"])

        same_country = db.session.query(Country).filter_by(name=new_country.name).first()

        if same_country:
            return abort(400, message="This country is already registered")

        Agency.get_instance().add_country(new_country)

        return new_country