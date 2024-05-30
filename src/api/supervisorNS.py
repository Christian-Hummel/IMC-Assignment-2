from flask import jsonify
from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, current_user
from werkzeug.security import generate_password_hash,check_password_hash

from ..model.agency import Agency
from ..database import Supervisor, TravelAgent, User, db

authorizations = {
    "authorizationToken":{
        "type":"apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

supervisor_ns = Namespace("supervisor", description="Supervisor related operations", authorizations=authorizations)

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
    "employee_id" : fields.Integer(required=True,
                                   help="The unique identifier of a supervisor"),
    "name" : fields.String(required=True,
                           help="The name of a supervisor, e.g. Charlie Brown"),
    "address" : fields.String(required=True,
                              help="The address of a supervisor, e.g. King's Street 4, 2910 London"),
    "email" : fields.String(required=True,
                            help="The email address of a supervisor, e.g. Charlie.Brown@hammertrips.com"),
    "salary" : fields.Integer(required=False,
                              help="The monthly salary of a supervisor, e.g. 10000"),
    "nationality" : fields.String(required=True,
                                  help="The nationality of a supervisor, e.g. Spain")
})

login_model = supervisor_ns.model("LoginModel",{
    "username": fields.String(required=True,
                              help="username of a supervisor, e.g. Clark Kent"),
    "password": fields.String(required=True,
                              help="password of the new user")
})

user_model = supervisor_ns.model("UserModel", {
    "id": fields.Integer(required=False,
                              help="unique identifier of a user"),
    "username": fields.String(required=False,
                              help="username of a supervisor account")
})

employee_model = supervisor_ns.model("EmployeeModel", {
    "name": fields.String(required=True,
                          help="name of a travel agent e.g. Jonathan Franks"),
    "address": fields.String(required=True,
                             help="address of a travel agent e.g. Mysterious Road 44, 3829 Los Angeles"),
    "salary": fields.Integer(required=False,
                             help="monthly salary of a travel agent, e.g. 20000"),
    "nationality": fields.String(required=True,
                                 help="nationality of a travel Agent e.g. Ecuador")
})

employee_output_model = supervisor_ns.model("EmployeeOutputModel", {
    "employee_id": fields.Integer(required=False,
                                  help="the unique identifier of a travel agent"),
    "name": fields.String(required=True,
                          help="name of a travel agent e.g. Jonathan Franks"),
    "address": fields.String(required=True,
                             help="address of a travel agent e.g. Mysterious Road 44, 3829 Los Angeles"),
    "email": fields.String(required=False,
                           help="email address of a travel agent e.g. Jonathan.Frank@hammertrips.com"),
    "salary": fields.Integer(required=False,
                             help="monthly salary of a travel agent, e.g. 20000"),
    "nationality": fields.String(required=True,
                                 help="nationality of a travel Agent e.g. Ecuador"),
    "supervisor_id": fields.Integer(required=False,
                                    help="unique identifier of the supervisor of this agent")
})

@supervisor_ns.route("/")
class SupervisorAPI(Resource):


    @supervisor_ns.doc(supervisor_input_model, description="Add a new supervisor")
    @supervisor_ns.expect(supervisor_input_model,validate=True)
    @supervisor_ns.marshal_with(supervisor_model, envelope="supervisor")
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
        # set role to supervisor
        new_supervisor.role = "supervisor"

        # transfer new supervisor to the agency
        Agency.get_instance().add_supervisor(new_supervisor)

        #return the supervisor
        return new_supervisor


@supervisor_ns.route("/<int:supervisor_id>/register")
class RegisterSupervisor(Resource):

    @supervisor_ns.doc(login_model,description="Add a new user")
    @supervisor_ns.expect(login_model,validate=True)
    @supervisor_ns.marshal_with(user_model, envelope="user")
    def post(self, supervisor_id):

        new_user = User(username=supervisor_ns.payload["username"],
                        password_hash=generate_password_hash(supervisor_ns.payload["password"]),
                        manager_id=supervisor_id)

        # check if manager already exists

        supervisor = db.session.query(Supervisor).filter_by(employee_id=new_user.manager_id).first()

        # check for username duplicate
        same_user = db.session.query(User).filter_by(username=new_user.username).first()

        if same_user: # throw an error if the username is already stored in the database
            return abort(400, message="This user already exists")

        elif not supervisor: #throw an error if the supervisor is not found in the database
            return abort(400, message="Supervisor not found")

        else: # forward user to agency if it does not already exist
            Agency.get_instance().register_user(new_user)
            new_user.id = db.session.query(User).count()
            return new_user


@supervisor_ns.route("/login")
class UserLogin(Resource):

    @supervisor_ns.doc(login_model,description="Log in for accessing more functionality")
    @supervisor_ns.expect(login_model,validate=True)
    def post(self):

        user = User.query.filter_by(username=supervisor_ns.payload["username"]).first()

        if not user:
            return abort(400, message="User does not exist")
        elif not check_password_hash(user.password_hash, supervisor_ns.payload["password"]):
            return abort(400, message="Incorrect Password")
        else:
            return {"access_token": create_access_token(user)}


@supervisor_ns.route("/<int:supervisor_id>/employee")
class EmployAgent(Resource):
    method_decorators = [jwt_required()]


    @supervisor_ns.doc(employee_model,description="Add a new travelAgent",security="authorizationToken")
    @supervisor_ns.expect(employee_model, validate=True)
    @supervisor_ns.marshal_with(employee_output_model, envelope="travelAgent")
    def post(self, supervisor_id):


        new_agent = TravelAgent(employee_id=id(self),
                                name=supervisor_ns.payload["name"],
                                address=supervisor_ns.payload["address"],
                                salary=supervisor_ns.payload["salary"],
                                nationality=supervisor_ns.payload["nationality"])


        # throw an error if the supervisor_id does not exist
        supervisor = db.session.query(Supervisor).filter_by(employee_id=supervisor_id).first()


        # set salary to a minimum if not set to a higher amount
        if new_agent.salary < 2000:
            new_agent.salary = 2000
        # throw an error if the salary is too high
        elif new_agent.salary > 4000:
            return abort(400, message="Please enter a salary amount in Euro from 2000 to 4000")
        # throw an error if the format of the name is not right
        if " " in new_agent.name:
            first, last = new_agent.name.split(" ")
            new_agent.email = f"{first}.{last}@hammertrips.com"
        else:
            return abort(400, message="Please insert your first and last name seperated by a space")
        # set role to supervisor
        new_agent.role = "travelAgent"

        # assign supervisor_id

        new_agent.supervisor_id = current_user.manager_id

        # transfer new supervisor to the agency
        Agency.get_instance().add_supervisor(new_agent)

        # return the supervisor
        return new_agent
