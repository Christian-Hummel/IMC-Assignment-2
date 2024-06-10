from flask import jsonify
from flask_restx import Namespace, Resource, fields, abort

from ..model.agency import Agency
from ..database import Customer, db

customer_ns = Namespace("customer", description="Customer related operations")

customer_input_model = customer_ns.model("CustomerInputModel", {
    "name": fields.String(required=True,
                          help="the name of a customer, e.g. Mick Jagger"),
    "address": fields.String(required=True,
                             help="the address of a customer, e.g. Rockefeller Street 4, 2739 New York"),
    "email": fields.String(required=True,
                           help="The unique email address of a customer, e.g. Paint.Black@Jagger.us"),
    "budget": fields.Integer(required=True,
                            help="The maximum amount of money a customer is willing to spend"),
    "preference": fields.String(required=False,
                                help="The preferred country the customer wants to visit")

})

customer_output_model = customer_ns.model("CustomerOutputModel", {
    "customer_id": fields.Integer(required=False,
                                  help="The unique identifier of a customer"),
    "name": fields.String(required=True,
                          help="the name of a customer, e.g. Mick Jagger"),
    "address": fields.String(required=True,
                             help="the address of a customer, e.g. Rockefeller Street 4, 2739 New York"),
    "email": fields.String(required=True,
                           help="The unique email address of a customer, e.g. Paint.Black@Jagger.us"),
    "budget": fields.Integer(required=True,
                            help="The maximum amount of money a customer is willing to spend"),
    "preference": fields.String(required=False,
                                help="The preferred country the customer wants to visit")

})


@customer_ns.route("/")
class CustomerAPI(Resource):

    @customer_ns.doc(customer_input_model, description="Add a customer to the agency")
    @customer_ns.expect(customer_input_model, validate=True)
    @customer_ns.marshal_with(customer_output_model, envelope="customer")
    def post(self):

        new_customer = Customer(customer_id=id(self),
                                name=customer_ns.payload["name"],
                                address=customer_ns.payload["address"],
                                email=customer_ns.payload["email"],
                                budget=customer_ns.payload["budget"],
                                )



        same_customer = db.session.query(Customer).filter_by(name=new_customer.name).first()

        if not same_customer:
            if customer_ns.payload["preference"] != "string":
                new_customer.preference = customer_ns.payload["preference"]
            elif customer_ns.payload["preference"] == "string":
                new_customer.preference = "None"

            if new_customer.budget <= 0:
                return abort(400, message="Please enter a valid budget")

            new_customer.agent_id = 0

            Agency.get_instance().register_customer(new_customer)
            return new_customer

        elif same_customer:
            return abort(400, message="Customer already registered")

@customer_ns.route("/<int:customer_id>/expert")
class CustomerExpert(Resource):

    @customer_ns.doc(description="Request an expert for the desired preference")
    def post(self, customer_id):

        customer = db.session.query(Customer).filter_by(customer_id=customer_id).one_or_none()

        if not customer:
            return abort(400, message="Customer not found")

        if customer:

            requested_customer = Agency.get_instance().request_expert(customer)

            if requested_customer:
                return jsonify(f"You have requested to be assisted by an expert of {requested_customer.preference}")
            elif not requested_customer:
                return abort(400, message="You have already requested an expert")

