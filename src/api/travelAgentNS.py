from flask import jsonify
from flask_restx import Namespace, Resource, fields, abort

from ..model.agency import Agency
from ..database import Supervisor, TravelAgent, Customer, Country, User, db


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