import os
from flask import Flask
from flask_restx import Api
from .model.agency import Agency
from .database import db
from .api.supervisorNS import supervisor_ns

agency = Agency()

def create_app(database_uri="sqlite:///travelbase.db"):
    travelroute_app = Flask(__name__)
    # Configure the database
    travelroute_app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    # Initialize database on app
    db.init_app(travelroute_app)


    # create db in current directory if not already present
    if not os.path.exists("instance/travelbase.db"):
        with travelroute_app.app_context():
            db.create_all()


    # need to extend this class for custom objects, so that they can be jsonified
    travelroute_api = Api(travelroute_app, title="Hammertrips: An App for booking journeys that you will not forget")

    # add individual namespaces
    travelroute_api.add_namespace(supervisor_ns)
    #travelroute_api.add_namespace(travelagent_ns)
    #travelroute_api.add_namespace(customer_ns)
    #travelroute_api.add_namespace(country_ns)


    return travelroute_app

if __name__ == '__main__':
    create_app().run(debug=False, port=7890)