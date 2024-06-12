from flask import jsonify
from flask_restx import Namespace, Resource, fields, abort

from ..model.agency import Agency
from ..database import Supervisor, TravelAgent, Offer, Customer, Country, User, db


travelAgent_ns = Namespace("travelAgent", description="TravelAgent related operations")

agent_update_model = travelAgent_ns.model("AgentUpdateModel", {
    "name": fields.String(required=True,
                          help="The name of a travelAgent, e.g. Bradley Cooper"),
    "address": fields.String(required=True,
                             help="The address of a travelAgent, e.g. Golden Beach 2, 3281 San Francisco")
})

agent_output_model = travelAgent_ns.model("AgentOutputModel", {
    "employee_id": fields.Integer(required=False,
                                  help="The unique identifier of a travelAgent"),
    "name": fields.String(required=True,
                          help="The name of a travelAgent, e.g. Bradley Cooper"),
    "address": fields.String(required=True,
                             help="The address of a travelAgent, e.g. Golden Beach 2, 3281 San Francisco"),
    "email": fields.String(required=False,
                           help="The email address of a travelAgent"),
    "nationality": fields.String(required=False,
                                 help="The nationality of a travelAgent, e.g. Norway"),
    "salary": fields.Integer(required=False,
                             help="The monthly salary of a travelAgent"),
    "supervisor_id": fields.Integer(required=False,
                                    help="The unique identifier of the supervisor of this TravelAgent")

})

offer_input_model = travelAgent_ns.model("OfferInputModel", {
    "offer_id": fields.Integer(required=False,
                               help="the unique identifier of an offer"),
    "customer_id": fields.Integer(required=True,
                                  help="the unique identifier of the customer"),
    "country": fields.String(required=True,
                             help="The name of the destination for the trip, e.g. Denmark"),
    "activities": fields.List(fields.Integer(),required=True,
                              help="Activities offered by the travelAgent for this country")
})

offer_output_model = travelAgent_ns.model("OfferOutputModel", {
    "offer_id": fields.Integer(required=False,
                               help="The unique identifier of an offer"),
    "total_price": fields.Integer(required=True,
                                  help="Total price of this trip offer"),
    "country": fields.String(required=True,
                             help="The name of the destination for the trip, e.g. Denmark"),
    "activities": fields.List(fields.String(), required=True,
                              help="Activities offered by the travelAgent for this country"),
    "customer_id": fields.Integer(required=False,
                                  help="The unique identifier of the recipiant"),
    "agent_id": fields.Integer(required=False,
                               help="The unique identifier of the sender of this offer"),
    "status": fields.String(required=False,
                            help="Status code of an offer, e.g. pending")
})




@travelAgent_ns.route("/<int:employee_id>/update")
class AgentUpdate(Resource):


    @travelAgent_ns.doc(agent_update_model, description="Update Personal Data of an Employee")
    @travelAgent_ns.expect(agent_update_model, validate=True)
    @travelAgent_ns.marshal_with(agent_output_model, envelope="travelAgent")
    def post(self, employee_id):
        # check if agent is registered in the agency
        targeted_agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).one_or_none()
        # throw an error if the agent is not registered

        # check if the format of the name is correct
        format = travelAgent_ns.payload["name"].split(" ")

        if len(format) == 1:
            return abort(400, message="Please enter first and last name seperated by a space")

        if not targeted_agent:
            return abort(400, message="TravelAgent not found")


        elif targeted_agent:

            updated_agent = TravelAgent(employee_id=targeted_agent.employee_id,
                                        name=travelAgent_ns.payload["name"],
                                        address=travelAgent_ns.payload["address"],
                                        email=targeted_agent.email,
                                        salary=targeted_agent.salary,
                                        nationality=targeted_agent.nationality,
                                        supervisor_id=targeted_agent.supervisor_id,
                                        )



            if updated_agent.name not in ["string", targeted_agent.name] or updated_agent.address not in ["string", targeted_agent.address]:
                Agency.get_instance().update_agent(employee_id,updated_agent)
                return updated_agent
            else:
                return abort(400, message="Please insert values to be updated")


@travelAgent_ns.route("/<int:employee_id>/offer")
class TravelAgentAPI(Resource):

    @travelAgent_ns.doc(offer_input_model, description="Send an offer to a customer")
    @travelAgent_ns.expect(offer_input_model, validate=True)
    @travelAgent_ns.marshal_with(offer_output_model, envelope="offer")
    def post(self, employee_id):

        offer_id = travelAgent_ns.payload["offer_id"]
        customer_id = travelAgent_ns.payload["customer_id"]
        country_name = travelAgent_ns.payload["country"]
        activ_ids = travelAgent_ns.payload["activities"]

        # existance checks

        agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).one_or_none()

        if not agent:
            return abort(400, message="TravelAgent not found")

        customer = db.session.query(Customer).filter_by(customer_id=customer_id).one_or_none()

        if not customer:
            return abort(400, message="Customer not found")

        country = db.session.query(Country).filter_by(name=country_name).one_or_none()

        if not country:
            return abort(400, message="Country not found")

        if offer_id == 0:

            new_offer = Offer(offer_id=id(self),
                              country=travelAgent_ns.payload["country"],
                              total_price=0,
                              status="pending",
                              customer_id=customer_id,
                              agent_id=employee_id
                              )

            for idx in activ_ids:
                if idx in [activ.activity_id for activ in country.activities]:
                        activity = [activity for activity in country.activities
                                    if activity.activity_id == idx]
                        new_offer.activities.append(activity[0])
                        new_offer.total_price += activity[0].price
                elif idx not in [activ.activity_id for activ in country.activities]:
                    return abort(400, message=f"Activity not registered for this country")

            # fix assignment of activities

            if customer.preference != "None":
                if new_offer.country != customer.preference:
                    return abort(400, message="This country does not match with the preference of your customer")

        elif offer_id != 0:

            offer = db.session.query(Offer).filter_by(offer_id=offer_id).one_or_none()

            if not offer:
                return abort(400, message="Offer not found")

            elif offer.agent_id != agent.agent_id:
                return abort(400, message="This offer was created by another TravelAgent")

            if offer.status == "resend":
                # country could be another, the travelAgent could offer a different country
                # with different activities to convince the customer
                new_offer = Offer(offer_id=offer_id,
                                  country=travelAgent_ns.payload["country"],
                                  total_price=0,
                                  customer_id=customer_id,
                                  agent_id=employee_id,
                                  status="changed")
                # empty existing activities list

                new_offer.activities = []

                # fix assignment of activities

                # fill it with the same or new activities -
                # allowed to be the same because the price could be lowered in the meantime

                for idx in activ_ids:
                    if idx in [activ.activity_id for activ in country.activities]:
                        activity = [activity for activity in country.activities if activity.activity_id == idx]
                        new_offer.activities.append(activity[0])
                        new_offer.total_price += activity[0].price
                    elif idx not in [activ.activity_id for activ in country.activities]:
                        return abort(400, message=f"Activity not registered for this country")

                if new_offer.country == "string" or new_offer.activities[0] == 0:
                    return abort(400, message="Invalid offer assignment")

            elif offer.status == "declined":
                return abort(400, message="This offer is already declined by the customer")


        offer_result = Agency.get_instance().present_offer(new_offer, agent, customer, country)

        if offer_result:
            return offer_result

        elif not offer_result:
            return abort(400, message="This offer exceeds the budget of the customer")


