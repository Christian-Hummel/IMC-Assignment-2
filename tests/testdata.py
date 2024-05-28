from src.model.agency import Agency
from src.database import Supervisor, TravelAgent, Customer, Country, Activity, db


def create_supervisors(agency: Agency):
    supervisor1 = Supervisor(employee_id=10, name="Alex Ferguson", address="Red Street 32, 3829 Manchester", email="Alex.Ferguson@hammertrips.com", salary=10000, nationality="Scotland", role="supervisor")
    db.session.add(supervisor1)
    db.session.commit()

def populate(agency: Agency):
    create_supervisors(agency)