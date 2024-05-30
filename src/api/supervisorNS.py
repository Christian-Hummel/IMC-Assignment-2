from flask import jsonify
from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash,check_password_hash

from ..model.agency import Agency
from ..database import Supervisor, User, db

#authorizations = {
    #"authorizationToken":{
        #"type":"apiKey",
        #"in": "header",
        #"name": "Authorization"
    #}
#}

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


@supervisor_ns.route("/")
class SupervisorAPI(Resource):
    #method_decorators = [jwt_required()]

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


