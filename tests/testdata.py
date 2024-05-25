from ..src.model.agency import Agency
from ..src.model.supervisor import Supervisor
from ..src.model.travelAgent import TravelAgent
from ..src.database import Employee, Customer, Country, Activity, db


def create_supervisors(agency: Agency):
    supervisor1 = Employee(employee_id=10, name="Alex Ferguson", address="Red Street 32, 3829 Manchester", email="Alex.Ferguson@hammertrips.com", salary=10000, nationality="Scotland", role="supervisor")
    db.session.add(supervisor1)
    db.session.commit()

def populate(agency: Agency):
    create_supervisors(agency)