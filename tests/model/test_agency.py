import pytest



from src.database import Supervisor, TravelAgent, Customer, Country, Activity, User, db



from tests.fixtures import app, client, agency

# Supervisor
def test_add_supervisor(agency):
        before = Supervisor.query.count()

        new_supervisor = Supervisor(employee_id= 12, name="Terry Pratchett", address="Penny Lane 23, 1255 Liverpool",email="John.Grisham@hammertrips.com", salary=8000, nationality="England")
        agency.add_supervisor(new_supervisor)

        supervisor = db.session.query(Supervisor).filter_by(employee_id = 12).first()


        assert Supervisor.query.count() == before + 1


        assert supervisor.name == "Terry Pratchett"
        assert supervisor.address == "Penny Lane 23, 1255 Liverpool"
        assert supervisor.email == "John.Grisham@hammertrips.com"
        assert supervisor.salary == 8000
        assert supervisor.nationality == "England"
        assert supervisor.role == "supervisor"


def test_register_supervisor(agency):
        before = User.query.count()

        new_user = User(username="Franz",password_hash="AJLSJERFHS")

        agency.register_user(new_user)

        target_user = db.session.query(User).filter_by(id=new_user.id).first()

        assert User.query.count() == before + 1

        assert target_user.username == "Franz"
        assert target_user.password_hash == "AJLSJERFHS"



def test_add_agent(agency):

        before = TravelAgent.query.count()


        new_agent = TravelAgent(employee_id=222,name="Sky DuMont",address="Alvaro 20,8573 Buenos Aires",email="Sky.DuMont@hammertrips.com",salary=3500,nationality="Germany",supervisor_id=135)

        agency.add_travelagent(new_agent)

        agent = db.session.query(TravelAgent).filter_by(employee_id=222).first()


        assert TravelAgent.query.count() == before + 1

        assert agent.name == "Sky DuMont"
        assert agent.address == "Alvaro 20,8573 Buenos Aires"
        assert agent.email == "Sky.DuMont@hammertrips.com"
        assert agent.salary == 3500
        assert agent.role == "travelAgent"
        assert agent.nationality == "Germany"
        assert agent.supervisor_id == 135


# TravelAgent


# Customer


# Country

def test_add_country(agency):

        before = Country.query.count()

        new_country = Country(country_id=976, name="Trinidad and Tobago")

        agency.add_country(new_country)

        country = db.session.query(Country).filter_by(country_id=976).first()

        assert Country.query.count() == before + 1

        assert country.name == "Trinidad and Tobago"





# Activity