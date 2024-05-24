from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields, abort

from ..model.agency import Agency
from ..model.supervisor import Supervisor


supervisor_ns = Namespace("supervisor", description="Supervisor related operations")

supervisor_input_model = supervisor_ns.model("SupervisorInputModel", {
    "name" : fields.String(required=True,
                           help="The name of a supervisor, e.g. Charlie Brown"),
    "address" : fields.String(required=True,
                              help="The address of a supervisor, e.g. King's Street 4, 2910 London"),
    "salary" : fields.Integer(required=False,
                              help="The monthly salary of a supervisor, e.g. 10000"),
    "nationality" : fields.String(required=True,
                                  help="The nationality of a supervisor, e.g. Spain")

})



supervisor_model = supervisor_ns.model("SupervisorModel", {
    "employee_id" : fields.Integer(required=False,
                                   help="The unique identifier of a supervisor"),
    "name" : fields.String(required=True,
                           help="The name of a supervisor, e.g. Charlie Brown"),
    "address" : fields.String(required=True,
                              help="The address of a supervisor, e.g. King's Street 4, 2910 London"),
    "email" : fields.String(required=False,
                            help="The email address of a supervisor, e.g. Charlie.Brown@hammertrips.com"),
    "salary" : fields.Integer(required=False,
                              help="The monthly salary of a supervisor, e.g. 10000"),
    "nationality" : fields.String(required=True,
                                  help="The nationality of a supervisor, e.g. Spain")
})


@supervisor_ns.route("/")
class SupervisorAPI(Resource):

    @supervisor_ns.doc(supervisor_input_model, description="Add a new supervisor")
    @supervisor_ns.expect(supervisor_input_model,validate=True)
    @supervisor_ns.marshal_with(supervisor_input_model, envelope="supervisor")
    def post(self):

        #Create a new Supervisor and add it

        new_supervisor = Supervisor(employee_id=id(self),
                                    name=supervisor_ns.payload["name"],
                                    address=supervisor_ns.payload["address"],
                                    salary=supervisor_ns.payload["salary"],
                                    nationality=supervisor_ns.payload["nationality"])

        # set salary to a minimum if not set to a higher amount
        if new_supervisor.salary < 8000:
            new_supervisor.salary = 8000
        # throw an error if the format of the name is not right
        if " " in new_supervisor.name:
            first,last = new_supervisor.name.split(" ")
            new_supervisor.email = f"{first}.{last}@hammertrips.com"
        else:
            return abort(400, message="Please insert your first and last name seperated by a space")

        # transfer new supervisor to the agency
        Agency.get_instance().add_supervisor(new_supervisor)

        #return the supervisor
        return new_supervisor


