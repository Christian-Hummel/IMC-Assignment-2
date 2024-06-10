from flask import jsonify
from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, current_user
from werkzeug.security import generate_password_hash,check_password_hash

from ..model.agency import Agency
from ..database import Supervisor, TravelAgent, Customer,  User, db

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


supervisor_info_model = supervisor_ns.model("SupervisorInfoModel", {
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
                                  help="The nationality of a supervisor, e.g. Spain"),
    "nr_of_teammembers" : fields.Integer(required=True,
                                         help="The number of people under his or her supervision")
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


agent_assign_model = supervisor_ns.model("AgentAssignModel",{
    "customer_id": fields.Integer(required=True,
                                  help="unique identifier of a registered customer")
})

customer_output_model = supervisor_ns.model("CustomerModel", {
    "customer_id": fields.Integer(required=True,
                                  help="unique identifier of a registered customer"),
    "name": fields.String(required=True,
                          help="The name of a customer, e.g. Harrison Ford"),
    "address": fields.String(required=True,
                             help="The address of a customer, e.g. Palm Beach 34, 2472 Miami"),
    "email": fields.String(required=True,
                           help="The email address of a customer"),
    "budget": fields.Integer(required=True,
                             help="The amount of money a customer is willing to spend for a trip"),
    "travel_agent_id": fields.Integer(required=True,
                                      help="The unique identifier of a TravelAgent this customer is assigned to")
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


        # check for duplicates
        same_supervisor = db.session.query(Supervisor).filter_by(name=new_supervisor.name).first()
        if not same_supervisor:

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

        elif same_supervisor:
            return abort(400, message="Supervisor already registered")

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

@supervisor_ns.route("/info")
class SupervisorInfo(Resource):
    method_decorators = [jwt_required()]

    @supervisor_ns.doc(description="Information about a supervisor", security="authorizationToken")
    @supervisor_ns.marshal_with(supervisor_info_model,envelope="supervisor")
    def get(self):


        supervisor = db.session.query(Supervisor).filter_by(employee_id=current_user.manager_id).first()
        # add number of people working in your team
        supervisor.nr_of_teammembers = len(supervisor.teammembers)
        # return the supervisor
        return supervisor

@supervisor_ns.route("/team")
class SupervisorAgents(Resource):
    method_decorators = [jwt_required()]

    @supervisor_ns.doc(employee_output_model, description="Get all agents under your supervision", security="authorizationToken")
    @supervisor_ns.marshal_list_with(employee_output_model, envelope="travelagents")
    def get(self):

        supervisor_id = current_user.manager_id
        # get team members
        team = Agency.get_instance().show_all_agents(supervisor_id)

        if team: # if there are travel agents in your team display them
            return team
        elif not team: # if there are no travel agents under your supervision yet throw an error
            return abort(400, message="There are no travel agents under your supervision yet")


@supervisor_ns.route("/<int:employee_id>/assign")
class SupervisorAssignments(Resource):
    method_decorators = [jwt_required()]


    @supervisor_ns.doc(agent_assign_model, description="Assign a TravelAgent to a Customer", security="authorizationToken")
    @supervisor_ns.expect(agent_assign_model,validate=True)
    def post(self, employee_id):

        customer_id = supervisor_ns.payload["customer_id"]
        supervisor_id = current_user.manager_id

        agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).one_or_none()
        customer = db.session.query(Customer).filter_by(customer_id=customer_id).first()




        if not agent: # throw an error if this agent is not registered in the agency
            return abort(400, message="TravelAgent not found")

        if not customer: # throw an error if this customer is not registered in the agency
            return abort(400, message="Customer not found")

        agent_id = agent.employee_id
        assignment = Agency.get_instance().assign_agent(customer_id,agent_id, supervisor_id)

        if assignment:
            return jsonify(f"TravelAgent {assignment[0].name} has been assigned to {assignment[1].name}")

        if not assignment:
            return abort(400,"This customer has already been assigned to a TravelAgent")

@supervisor_ns.route("/customers")
class AgencyCustomers(Resource):
    method_decorators = [jwt_required()]

    @supervisor_ns.doc(customer_output_model, description="Get information about all customers",security="authorizationToken")
    @supervisor_ns.marshal_list_with(customer_output_model, envelope="customers")
    def get(self):

        customers = Agency.get_instance().get_all_customers()

        if customers:
            return customers

        if not customers:
            return abort(400, message="There are no customers currently registered")