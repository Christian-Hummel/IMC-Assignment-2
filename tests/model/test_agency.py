import pytest



from src.database import Supervisor, TravelAgent, Customer, Offer, Country, Activity, User, db



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



def test_get_supervisor_info(agency):

        supervisor = db.session.query(Supervisor).filter_by(employee_id=78).first()

        supervisor_id = supervisor.employee_id

        supervisor_info = agency.get_supervisor_by_id(supervisor_id)

        assert supervisor_info.name == "Robert Downey Jr."
        assert supervisor_info.address == "404 Willow Way, Coast City"
        assert supervisor_info.email == "Robert.Downey@hammertrips.com"
        assert supervisor_info.salary == 28945
        assert supervisor_info.nationality == "USA"
        assert supervisor_info.nr_of_teammembers == 1

def test_get_supervisor_info_error(agency):

        result_supervisor = agency.get_supervisor_by_id(439)

        assert not result_supervisor

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

def test_assign_agent_nexpertpreference(agency):

        supervisor = db.session.query(User).filter_by(id=5).first()

        supervisor_id = supervisor.manager_id

        agent = db.session.query(TravelAgent).filter_by(employee_id=255).first()

        before = len(agent.customers)

        employee_id = agent.employee_id

        customer = db.session.query(Customer).filter_by(customer_id=719).first()

        customer_id = customer.customer_id

        assignment = agency.assign_agent(customer_id,employee_id,supervisor_id)

        ragent,rcustomer = assignment

        assert len(ragent.customers) == before + 1

        assert ragent.name == "Jane Smith"

        assert rcustomer.name == "Alfred Nobel"
        assert rcustomer.agent_id == 255


def test_assign_agent_expert(agency):

        supervisor = db.session.query(User).filter_by(id=3).first()

        supervisor_id = supervisor.manager_id

        agent = db.session.query(TravelAgent).filter_by(employee_id=245).first()

        before = len(agent.customers)

        employee_id = agent.employee_id

        customer = db.session.query(Customer).filter_by(customer_id=720).first()

        customer_id = customer.customer_id

        assignment = agency.assign_agent(customer_id,employee_id,supervisor_id)

        ragent,rcustomer = assignment

        assert len(ragent.customers) == before + 1

        assert ragent.name == "Philipp Lienhart"

        assert rcustomer.name == "Marie Tharp"
        assert rcustomer.agent_id == 245


def test_assign_agent_nexpertnpreference(agency):

        supervisor = db.session.query(User).filter_by(id=2).first()

        supervisor_id = supervisor.manager_id

        agent = db.session.query(TravelAgent).filter_by(employee_id=240).first()

        before = len(agent.customers)

        employee_id = agent.employee_id

        customer = db.session.query(Customer).filter_by(customer_id=717).first()

        customer_id = customer.customer_id

        assignment = agency.assign_agent(customer_id,employee_id,supervisor_id)

        ragent,rcustomer = assignment

        assert len(ragent.customers) == before + 1

        assert ragent.name == "Christopher Lee"

        assert rcustomer.name == "Rosalind Franklin"
        assert rcustomer.agent_id == 240


def test_assign_agent_errors(agency):

        supervisor = db.session.query(User).filter_by(id=3).first()

        supervisor_id = supervisor.manager_id

        agent = db.session.query(TravelAgent).filter_by(employee_id=245).first()

        before = len(agent.customers)

        employee_id = agent.employee_id

        customer = db.session.query(Customer).filter_by(customer_id=718).first()

        customer_id = customer.customer_id

        already_assigned = agency.assign_agent(customer_id,employee_id,supervisor_id)

        # check return value of function call - None in this case
        assert not already_assigned

        with pytest.raises(Exception,match="This agent is not a member of your team"):
                agency.assign_agent(716,255,102)

        with pytest.raises(Exception,match="This TravelAgent does not have the required expert status"):
                agency.assign_agent(720,280,102)

        with pytest.raises(Exception,match="This TravelAgent is not assigned to the preferred country"):
                agency.assign_agent(719,315,179)



def test_get_all_customers(agency):

        count = Customer.query.count()

        customers = agency.get_all_customers()

        assert count == len(customers)

def test_get_all_customers_error(agency):
        empty = db.session.query(Customer).delete()

        customers = agency.get_all_customers()

        assert not customers

def test_get_customer_by_id(agency):

        customer = agency.get_customer_by_id(720)

        assert customer.name == "Marie Tharp"
        assert customer.address == "Ocean Avenue 4, 1001 New York"
        assert customer.email == "Marie.Tharp@geology.us"
        assert customer.budget == 21000
        assert customer.preference == "Austria"
        assert customer.expert
        assert customer.agent_id == 0

def test_get_customer_by_id_error(agency):

        customer = agency.get_customer_by_id(493)

        assert not customer


def test_get_agent_by_id(agency):

        agent = db.session.query(TravelAgent).filter_by(employee_id=255).first()

        employee_id = agent.employee_id

        agent_info = agency.get_agent_by_id(employee_id)

        assert agent_info.name == "Jane Smith"
        assert agent_info.address == "Elm Street 12, 5678 Gotham"
        assert agent.email == "Jane.Smith@hammertrips.com"
        assert agent.salary == 3200
        assert agent.nationality == "Canada"
        assert len(agent.countries) == 3
        assert len(agent.customers) == 1
        assert agent.supervisor_id == 56


def test_get_agent_by_id_error(agency):


        agent_result = agency.get_agent_by_id(463)

        assert not agent_result

def test_increase_agent_salary(agency):

        supervisor = db.session.query(Supervisor).filter_by(employee_id=91).first()

        agent = db.session.query(TravelAgent).filter_by(employee_id=275).first()

        supervisor_id = supervisor.employee_id

        employee_id = agent.employee_id

        increase = 0.05

        assert agent.salary == 3200

        result = agency.increase_agent_salary(supervisor_id,employee_id,increase)

        assert result.name == "Sarah Wilson"
        assert result.salary == 3360

def test_increase_agent_salary_error(agency):

        supervisor = db.session.query(Supervisor).filter_by(employee_id=91).first()

        agent = db.session.query(TravelAgent).filter_by(employee_id=250).first()

        supervisor_id = supervisor.employee_id

        employee_id = agent.employee_id

        increase = 0.05

        result = agency.increase_agent_salary(supervisor_id,employee_id,increase)

        assert not result

def test_assign_country(agency):

        supervisor = db.session.query(Supervisor).filter_by(employee_id=113).first()
        agent = db.session.query(TravelAgent).filter_by(employee_id=285).first()
        country = db.session.query(Country).filter_by(country_id=909).first()

        before = len(agent.countries)

        result = agency.assign_country(country,agent,supervisor)

        assert result.name == "Emma Taylor"
        assert len(agent.countries) == before + 1

def test_assign_country_errors(agency):

        supervisor = db.session.query(Supervisor).filter_by(employee_id=135).first()
        assigned_agent = db.session.query(TravelAgent).filter_by(employee_id=295).first()
        assigned_country = db.session.query(Country).filter_by(country_id=901).first()
        diff_agent = db.session.query(TravelAgent).filter_by(employee_id= 270).first()

        with pytest.raises(Exception, match="This country is already registered for this TravelAgent"):
                agency.assign_country(assigned_country,assigned_agent,supervisor)

        result = agency.assign_country(assigned_country,diff_agent,supervisor)

        assert not result

def test_get_agent_stats(agency):

        agent = db.session.query(TravelAgent).filter_by(employee_id=255).first()

        employee_id = agent.employee_id

        result = agency.get_agent_stats(employee_id)

        assert result.stats_id == 33
        assert result.agent_id == 255
        assert result.num_customers == 2
        assert result.num_trips == 0
        assert result.total_revenue == 0

def test_get_agent_stats_error(agency):

        agent = db.session.query(TravelAgent).filter_by(employee_id=360).first()
        employee_id = agent.employee_id

        result = agency.get_agent_stats(employee_id)

        assert not result

# TravelAgent

## do not need a test for update_agent, because sqlalchemy is already tested

def test_present_new_offer(agency):

        new_offer = Offer(offer_id=833, country="Spain", total_price=96, status="pending", agent_id=310, customer_id=715)
        activity1 = db.session.query(Activity).filter_by(activity_id=611).first()
        activity2 = db.session.query(Activity).filter_by(activity_id=613).first()
        new_offer.activities.extend([activity1, activity2])
        customer = db.session.query(Customer).filter_by(customer_id=715).first()

        before = Offer.query.count()

        result = agency.present_offer(new_offer,customer)

        assert len(db.session.query(Offer).all()) == before + 1

        assert result.offer_id == 833
        assert result.country == "Spain"
        assert result.total_price == 96
        assert result.status == "pending"
        assert result.agent_id == 310
        assert result.customer_id == 715





def test_present_changed_offer(agency):

        before = Offer.query.count()
        offer = db.session.query(Offer).filter_by(offer_id=810).first()

        assert len(offer.activities) == 1

        offer.activities = []
        activity1 = db.session.query(Activity).filter_by(activity_id=611).first()
        activity2 = db.session.query(Activity).filter_by(activity_id=613).first()
        offer.activities.extend([activity1, activity2])
        offer.total_price = 96
        customer = db.session.query(Customer).filter_by(customer_id=715).first()

        result = agency.present_offer(offer, customer)

        assert len(db.session.query(Offer).all()) == before
        assert len(offer.activities) == 2

        assert result.offer_id == 810
        assert result.country == "Spain"
        assert result.total_price == 96
        assert result.status == "changed"
        assert result.agent_id == 310
        assert result.customer_id == 715



def test_present_offer_errors(agency):

        # new offer - budget

        before1 = Offer.query.count()
        customer1 = db.session.query(Customer).filter_by(customer_id=713).first()

        new_offer = Offer(offer_id=845, country="France", total_price=2030, status="pending", agent_id=300, customer_id=713)
        activity1 = db.session.query(Activity).filter_by(activity_id=602).first()
        activity2 = db.session.query(Activity).filter_by(activity_id=616).first()
        new_offer.activities.extend([activity1, activity2])

        result1 = agency.present_offer(new_offer,customer1)

        assert not result1

        assert len(db.session.query(Offer).all()) == before1 + 1



        # changed offer - budget
        before2 = Offer.query.count()
        offer = db.session.query(Offer).filter_by(offer_id=808).first()

        customer2 = db.session.query(Customer).filter_by(customer_id=715).first()


        offer.activities = []
        activity = db.session.query(Activity).filter_by(activity_id=616).first()
        offer.activities.append(activity)
        offer.total_price = 2000

        assert offer.status == "changed"

        result2 = agency.present_offer(offer,customer2)

        assert not result2

        assert len(db.session.query(Offer).all()) == before2

        assert offer.status == "budget"




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


def test_request_expert(agency):

        customer = db.session.query(Customer).filter_by(customer_id=712).first()

        assert not customer.expert

        expert_request = agency.request_expert(customer)

        assert expert_request.name == "Thomas Edison"
        assert expert_request.expert



def test_request_expert_errors(agency):

        customer1 = db.session.query(Customer).filter_by(customer_id=709).first()

        expert_result = agency.request_expert(customer1)

        assert not expert_result

        customer2 = db.session.query(Customer).filter_by(customer_id=716).first()

        with pytest.raises(ValueError,match="No country registered as a preference"):
                agency.request_expert(customer2)

def test_show_offers(agency):

        customer = db.session.query(Customer).filter_by(customer_id=713).first()
        customer_id = customer.customer_id

        assert len(customer.offers) == 3

        result = agency.show_offers(customer_id)

        # only one of them is valid
        assert len(result) == 1

def test_show_offers_errors(agency):

        customer1 = db.session.query(Customer).filter_by(customer_id=703).first()
        customer_id1 = customer1.customer_id

        result1 = agency.show_offers(customer_id1)

        assert not result1

        customer2 = db.session.query(Customer).filter_by(customer_id=716).first()
        customer_id2 = customer2.customer_id

        result2 = agency.show_offers(customer_id2)

        assert not result2

def test_handle_offer(agency):

        offer1 = db.session.query(Offer).filter_by(offer_id=806).first()
        offer2 = db.session.query(Offer).filter_by(offer_id=815).first()
        offer3 = db.session.query(Offer).filter_by(offer_id=816).first()

        result1 = agency.handle_offer("accept",offer1)

        assert result1.status == "accepted"

        result2 = agency.handle_offer("change",offer2)

        assert result2.status == "resend"

        result3 = agency.handle_offer("decline", offer3)

        assert result3.status == "declined"



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

        assert count == len(countries)

def test_get_all_countries_error(agency):

        empty = db.session.query(Country).delete()
        db.session.commit()


        result = agency.get_all_countries()

        assert not result


def test_get_country_by_id(agency):

        country = agency.get_country_by_id(919)

        assert country["country_id"] == 919
        assert country["name"] == "Netherlands"
        assert len(country["activities"]) == 0

# Activity

def test_add_activity(agency):

        country = db.session.query(Country).filter_by(name="Germany").first()

        country_id = country.country_id

        before = len(country.activities)

        new_activity = Activity(activity_id=934,name="Jetski",price=100)

        agency.add_activity(new_activity,country_id)

        assert len(country.activities) == before + 1


def test_add_activity_error(agency):

        new_activity = Activity(activity_id=333, name="Miniatur Wunderland", price=20)

        with pytest.raises(Exception, match="This activity is already registered for this country"):
                agency.add_activity(new_activity,901)


def test_update_activity(agency):


        new_activity = Activity(activity_id=899, name="Mountain Tour", price=60)

        agency.add_activity(new_activity, 901)

        country = db.session.query(Country).filter_by(country_id=901).first()

        activity_match = [activity for activity in country.activities if activity.activity_id == 899]
        activity = activity_match[0]

        assert activity.name == "Mountain Tour"
        assert activity.price == 60

        update_activity = Activity(activity_id=899, name="Alps Expedition", price=130)

        agency.update_activity(update_activity,901)

        assert activity.name == "Alps Expedition"
        assert activity.price == 130

def test_update_activity_errors(agency):


        invalid_price = Activity(activity_id=609, name="Safar", price=0)

        with pytest.raises(ValueError,match="Invalid Price"):
                agency.update_activity(invalid_price,909)


def test_remove_activity(agency):

        country = db.session.query(Country).filter_by(country_id=911).first()
        activity = db.session.query(Activity).filter_by(activity_id=611).first()


        assert "Stadion Tour" in [activity.name for activity in country.activities]

        result = agency.remove_activity(country,activity)

        assert not "Stadion Tour" in [activity.name for activity in country.activities]

def test_remove_activity_error(agency):

        country = db.session.query(Country).filter_by(country_id=911).first()
        activity = db.session.query(Activity).filter_by(activity_id=613).first()

        result = agency.remove_activity(country,activity)

        assert not result

def test_get_activity_by_id(agency):

        country = db.session.query(Country).filter_by(country_id=911).first()
        activity = db.session.query(Activity).filter_by(activity_id=611).first()

        country_id = country.country_id
        activity_id = activity.activity_id

        result = agency.get_activity_by_id(activity_id,country_id)

        assert result.activity_id == 611
        assert result.name == "Stadion Tour"
        assert result.price == 70

def test_get_activity_by_id_errors(agency):

        country = db.session.query(Country).filter_by(country_id=904).first()
        activity = db.session.query(Activity).filter_by(activity_id=612).first()

        country_id = country.country_id
        activity_id = activity.activity_id

        with pytest.raises(Exception, match="Activity not found"):
                agency.get_activity_by_id(823,country_id)

        result = agency.get_activity_by_id(activity_id, country_id)

        assert not result
