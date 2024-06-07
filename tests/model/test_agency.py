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



def test_get_supervisor_agents(agency):

        supervisor = db.session.query(Supervisor).filter_by(employee_id=135).first()

        supervisor_id = supervisor.employee_id

        team = agency.show_all_agents(supervisor_id)

        assert len(team) == 1

def test_get_supervisor_agents_no_teammembers(agency):

        supervisor = db.session.query(User).filter_by(id=1).first()


        supervisor_id = supervisor.manager_id

        team = agency.show_all_agents(supervisor_id)

        assert not team


# TravelAgent


# Customer

def test_register_customer(agency):

        before = Customer.query.count()

        new_customer = Customer(customer_id=695, name="Steve Backshall", address="Rocky road 4, 3627 Sidney", email="Steve@bbc.co.uk", budget=17000, preference="Japan",agent_id=0)

        agency.register_customer(new_customer)

        customer = db.session.query(Customer).filter_by(customer_id=695).first()

        assert Customer.query.count() == before + 1

        assert customer.name == "Steve Backshall"
        assert customer.address == "Rocky road 4, 3627 Sidney"
        assert customer.email == "Steve@bbc.co.uk"
        assert customer.preference == "Japan"
        assert customer.budget == 17000
        assert customer.agent_id == 0






# Country

def test_add_country(agency):

        before = Country.query.count()

        new_country = Country(country_id=976, name="Trinidad and Tobago")

        agency.add_country(new_country)

        country = db.session.query(Country).filter_by(country_id=976).first()

        assert Country.query.count() == before + 1

        assert country.name == "Trinidad and Tobago"


def test_get_all_countries(agency):

        count = Country.query.count()

        countries = agency.get_all_countries()

        assert len(countries) == count

def test_get_all_countries_error(agency):

        empty = db.session.query(Country).delete()
        db.session.commit()


        with pytest.raises(Exception,match="There are no countries registered"):
                agency.get_all_countries()



def test_get_country_by_id(agency):

        country = agency.get_country_by_id(919)

        assert country["country_id"] == 919
        assert country["name"] == "Netherlands"
        assert len(country["activities"]) == 0

# Activity