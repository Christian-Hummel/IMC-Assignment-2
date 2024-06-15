from flask import jsonify
from flask_restx import Namespace, Resource, fields, abort

from ..model.agency import Agency
from ..database import TravelAgent, Offer, Customer, Country, db


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


offer_discount_model = travelAgent_ns.model("OfferDiscountModel", {
    "percentage":fields.Integer(required=True,
                   help="Percentage of the requested discount for an offer")
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

        global offer_result
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

        if not country or travelAgent_ns.payload["country"] == "string":
            return abort(400, message="Country not found")

        # check if customer is registered for this TravelAgent
        if customer not in agent.customers:
            return abort(400, message="This customer is not assigned to you")

        # check if country is registered for this TravelAgent
        if country not in agent.countries:
            return abort(400,message="This country is not assigned to you")

        if offer_id == 0:


            new_offer = Offer(offer_id=id(self),
                              country=travelAgent_ns.payload["country"],
                              total_price=0,
                              status="pending",
                              customer_id=customer_id,
                              agent_id=employee_id
                              )

            # assignment of activities
            if activ_ids[0] != 0:
                for idx in activ_ids:
                    if idx in [activ.activity_id for activ in country.activities]:
                            activity = [activity for activity in country.activities
                                        if activity.activity_id == idx]
                            new_offer.activities.append(activity[0])
                            new_offer.total_price += activity[0].price
                    elif idx not in [activ.activity_id for activ in country.activities]:
                        db.session.rollback()
                        return abort(400, message=f"Activity with id {idx} not registered for this country")
            elif activ_ids[0] == 0:
                return abort(400, message="Please insert activities for your offer")

            if customer.preference != "None" and new_offer.country != customer.preference:
                return abort(400, message="This country does not match with the preference of your customer")

            offer_result = Agency.get_instance().present_offer(new_offer, customer)

        elif offer_id != 0:

            update_offer = db.session.query(Offer).filter_by(offer_id=offer_id).one_or_none()

            if not update_offer:
                return abort(400, message="Offer not found")

            elif update_offer.agent_id != agent.employee_id:
                return abort(400, message="This offer was created by another TravelAgent")

            if update_offer.status == "resend":

                # country could be a different one from the previous offer, the travelAgent could offer a different country
                # with different activities to convince the customer

                update_offer.country = travelAgent_ns.payload["country"]
                # reset the price so it can be calculated again
                update_offer.total_price = 0
                # empty existing activities list
                update_offer.activities = []

                # (re)assignment of activities
                # fill it with the same or new activities
                # allowed to be the same because the price could have been lowered in the meantime
                if activ_ids[0] != 0:
                    for idx in activ_ids:
                        if idx in [activ.activity_id for activ in country.activities]:
                            activity = [activity for activity in country.activities if activity.activity_id == idx]
                            update_offer.activities.append(activity[0])
                            update_offer.total_price += activity[0].price
                        elif idx not in [activ.activity_id for activ in country.activities]:
                            db.session.rollback()
                            return abort(400, message=f"Activity with id {idx} not registered for this country")
                elif activ_ids[0] == 0:
                    return abort(400, message="Please insert activities for your offer")


                update_offer.status = "changed"

                offer_result = Agency.get_instance().present_offer(update_offer, customer)

            elif update_offer.status == "budget":
                return abort(400, message="This offer exceeds the budget contact your supervisor")

            elif update_offer.status == "pending":
                return abort(400, message="This offer is still pending, please wait for a response")

            elif update_offer.status == "declined":
                return abort(400, message="This offer is already declined by the customer")


        if offer_result:
            return offer_result


        elif not offer_result:
            db.session.rollback()
            return abort(400, message="This offer exceeds the budget of the customer")

    @travelAgent_ns.doc(offer_output_model, description="Get information about all offers from this TravelAgent")
    @travelAgent_ns.marshal_list_with(offer_output_model, envelope="offers")
    def get(self, employee_id):

        agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).one_or_none()

        if not agent:
            return abort(400, message="TravelAgent not found")

        offers = Agency.get_instance().get_all_offers(employee_id)

        if offers:
            return offers
        elif not offers:
            return abort(400, message="There are no Offers created by you")


@travelAgent_ns.route("/<int:employee_id>/raise")
class RequestRaise(Resource):

    @travelAgent_ns.doc(description="Request a raise in salary from your supervisor")
    def post(self, employee_id):

        agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).one_or_none()

        if not agent:
            return abort(400, message="TravelAgent not found")

        result = Agency.get_instance().request_raise(agent)

        if result:
            return jsonify(result)

        if not result:
            return abort(400,"Request for raise still pending")



@travelAgent_ns.route("/<int:employee_id>/offer/<int:offer_id>/discount")
class RequestDiscount(Resource):

    @travelAgent_ns.doc(offer_discount_model,description="Request a discount for the total cost of a trip")
    @travelAgent_ns.expect(offer_discount_model, validate=True)
    def post(self, employee_id,offer_id):

        percentage = travelAgent_ns.payload["percentage"]
        agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).one_or_none()
        offer = db.session.query(Offer).filter_by(offer_id=offer_id).one_or_none()


        if percentage <= 0 or percentage > 40:
            return abort(400, message="Please insert a valid percentage in the range from 1 to 40")

        if not agent:
            return abort(400, message="TravelAgent not found")

        if not offer:
            return abort(400, message="Offer not found")

        if offer.agent_id != agent.employee_id:
            return abort(400, message="This offer is not one of yours")

        if offer.status != "budget":
            return abort(400, message="This offer is not available for discounts")

        result = Agency.get_instance().request_discount(agent,offer,percentage)

        if result:
            return jsonify(result)
        if not result:
            return abort(400, message="The request for lowering this offer is still pending")




