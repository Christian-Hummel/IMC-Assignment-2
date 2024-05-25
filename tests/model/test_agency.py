import pytest


from src.model.supervisor import Supervisor
from src.model.travelAgent import TravelAgent
#from ...src.model.customer import Customer
#from ...src.model.country import Country
#from ...src.model.activity import Activity

from src.database import Employee, Customer, Country, Activity, db



from tests.fixtures import app, client, agency


def test_add_supervisor(agency):
        new_supervisor = Supervisor(employee_id= 12, name="John Grisham", address="Penny Lane 23, 1255 Liverpool", salary=8000, nationality="England")
        new_supervisor.email = "John.Grisham@hammertrips.com"
        agency.add_supervisor(new_supervisor)

        print(db.session.scalars(db.select(Employee)).filter_by(employee_id=12))



