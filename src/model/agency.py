from typing import List, Union, Optional


from ..database import Supervisor, TravelAgent, Offer, Customer, Country, Activity, User, db





class Agency(object):
    singleton_instance = None


    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance


# Supervisor

    def add_supervisor(self, new_supervisor:Supervisor):

        db.session.add(new_supervisor)
        db.session.commit()


    def register_user(self, new_user:User):

        db.session.add(new_user)
        db.session.commit()


    def add_travelagent(self, new_agent: TravelAgent):

        expert = new_agent.nationality
        # check if the country of the expert status already exists
        expert_country = db.session.query(Country).filter_by(name=expert).one_or_none()

        # register expert country if it is already in the agency
        if expert_country:
            new_agent.countries.append(expert_country)

        # register country if it does not exist
        elif not expert_country:
            new_country = Country(country_id=id(self),name=expert)
            db.session.add(new_country)
            new_agent.countries.append(new_country)

        db.session.add(new_agent)
        db.session.commit()


    def get_supervisor_by_id(self, supervisor_id):

        supervisor = db.session.query(Supervisor).filter_by(employee_id=supervisor_id).one_or_none()

        if supervisor:
            # add number of people working in the team
            supervisor.nr_of_teammembers = len(supervisor.teammembers)
            # return the supervisor
            return supervisor

        elif not supervisor:
            return None

    def show_all_agents(self,supervisor_id):

        supervisor = db.session.query(Supervisor).filter_by(employee_id=supervisor_id).first()

        if hasattr(supervisor, "teammembers"):
            team = supervisor.teammembers

            return team
        else:
            return None

    def get_agent_by_id(self, employee_id):

        agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).one_or_none()

        if agent:
            return agent

        elif not agent:
            return None




    def assign_agent(self, customer_id, agent_id, supervisor_id):

        customer = db.session.query(Customer).filter_by(customer_id=customer_id).first()
        agent = db.session.query(TravelAgent).filter_by(employee_id=agent_id).first()
        supervisor = db.session.query(Supervisor).filter_by(employee_id=supervisor_id).first()


        employee_id = agent.employee_id

        if agent not in supervisor.teammembers:
            raise Exception("This agent is not a member of your team")

        if customer.agent_id == 0:
            # customer requires an expert for a specific country
            if customer.expert and customer.preference == agent.nationality:
                for agent in supervisor.teammembers:
                    if agent.employee_id == employee_id:
                        customer.agent_id = employee_id
                        db.session.commit()
                        return [agent,customer]
            elif customer.expert and agent.nationality != customer.preference:
                raise Exception("This TravelAgent does not have the required expert status")
            # customer does not require an expert and does not have any preferences
            elif not customer.expert and customer.preference == "None":
                for agent in supervisor.teammembers:
                    if agent.employee_id == employee_id:
                        customer.agent_id = employee_id
                        db.session.commit()
                        return [agent,customer]
            # customer does not require an expert but has got a preference
            elif not customer.expert and customer.preference != "None":
                for agent in supervisor.teammembers:
                    if agent.employee_id == employee_id and customer.preference in [country.name for country in agent.countries]:
                        customer.agent_id = employee_id
                        db.session.commit()
                        return [agent,customer]
                    elif customer.preference not in [country.name for country in agent.countries]:
                        raise Exception("This TravelAgent is not assigned to the preferred country")
        # if there is already a TravelAgent assigned to this person throw an error
        elif customer.agent_id != 0:
            return None

    def get_all_customers(self):

        customers = db.session.query(Customer).all()

        if len(customers):
            return customers
        elif not len(customers):
            return None

    def get_customer_by_id(self,customer_id):

        customer = db.session.query(Customer).filter_by(customer_id=customer_id).one_or_none()

        if customer:
            return customer
        elif not customer:
            return None


    def increase_agent_salary(self,supervisor_id,employee_id,increase):

        agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).first()

        supervisor = db.session.query(Supervisor).filter_by(employee_id=supervisor_id).first()

        if agent not in supervisor.teammembers:
            return None

        elif agent in supervisor.teammembers:

            agent.salary = agent.salary * (1 + increase)
            db.session.commit()

            return agent

    def assign_country(self, country:Country, agent:TravelAgent, supervisor:Supervisor):

        if agent not in supervisor.teammembers:
            return None

        if country not in agent.countries:
            agent.countries.append(country)
            db.session.commit()
            return agent

        elif country in agent.countries:
            raise Exception("This country is already registered for this TravelAgent")

# TravelAgent

    def update_agent(self,employee_id,updated_agent:TravelAgent):

        agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).first()

        agent.name = updated_agent.name
        agent.address = updated_agent.address
        db.session.commit()


    def present_offer(self, new_offer:Offer, customer:Customer):


        # check if the trip is affordable for the customer
        if new_offer.total_price <= customer.budget and new_offer.status == "pending":
            db.session.add(new_offer)
            db.session.commit()
            return new_offer
        elif new_offer.total_price <= customer.budget and new_offer.status == "changed":
            # works even without this
            # db.session.commit()
            return new_offer
        elif new_offer.total_price > customer.budget and new_offer.status == "pending":
            new_offer.status = "budget"
            db.session.add(new_offer)
            db.session.commit()
            return None
        elif new_offer.total_price > customer.budget and new_offer.status == "changed":
            new_offer.status = "budget"
            # db.session.commit()
            return None



# Customer

    def register_customer(self, new_customer:Customer):

        db.session.add(new_customer)
        db.session.commit()


    def request_expert(self, customer:Customer):

        if customer.preference == "None":
            raise ValueError("No country registered as a preference")

        elif customer.preference != "None" and not customer.expert:
            customer.expert = True
            db.session.commit()
            return customer
        else:
            return None

    def show_offers(self, customer_id):

        offers = db.session.query(Offer).filter_by(customer_id=customer_id).all()

        if not len(offers):
            return None

        if len(offers):
            result = [offer for offer in offers if offer.status in ["pending","changed"]]

            if len(result):
                return result
            elif not len(result):
                return None

# Country

    def add_country(self, new_country:Country):

        db.session.add(new_country)
        db.session.commit()


    def get_all_countries(self):

        countries = db.session.query(Country).order_by(Country.name).all()

        if len(countries):
            return countries
        elif not len(countries):
            return None


    def get_country_by_id(self, country_id:int):

        country = db.session.query(Country).filter_by(country_id=country_id).first()


        if country:

            country_json = {
                "country_id": country.country_id,
                "name": country.name,
                "activities": [f"Name: {activity.name} Price: {activity.price} ID: {activity.activity_id} " for activity in country.activities]
            }

            return country_json
        elif not country:
            return None


# Activity


    def add_activity(self, new_activity: Activity,country_id):

        # filter out corresponding country
        country = db.session.query(Country).filter_by(country_id=country_id).first()
        # check if activity is already registered for this country
        for activity in country.activities:
            if activity.name == new_activity.name:
                raise Exception("This activity is already registered for this country")

        # check if this activity is already registered for another country
        same_activity = db.session.query(Activity).filter_by(name=new_activity.name).first()


        if same_activity: # update id to already existing id
            same_activity.price = new_activity.price
            country.activities.append(same_activity)
            db.session.commit()

        # add activity with new id if it is not registered yet
        elif not same_activity:
            country.activities.append(new_activity)
            # add activity to the database
            db.session.add(new_activity)
            db.session.commit()


    def update_activity(self, updated_activity: Activity, country_id):

        if updated_activity.price <= 0:
            raise ValueError("Invalid Price")

        # if this activity is already in the Activity table by this name, update the activity id
        same_name = db.session.query(Activity).filter_by(name=updated_activity.name).first()
        if same_name:
            updated_activity.activity_id = same_name.activity_id

        country = db.session.query(Country).filter_by(country_id=country_id).first()

        for activity in country.activities:
            if activity.activity_id == updated_activity.activity_id:
                activity.name = updated_activity.name
                activity.price = updated_activity.price
                db.session.commit()


    def remove_activity(self, country:Country, r_activity:Activity):

        for activity in country.activities:
            if activity.activity_id == r_activity.activity_id:
                country.activities.remove(activity)
                db.session.commit()
                return country
        return None

    def get_activity_by_id(self, activity_id, country_id):

        country = db.session.query(Country).filter_by(country_id=country_id).first()

        activity = db.session.query(Activity).filter_by(activity_id=activity_id).one_or_none()

        if not activity:
            raise Exception("Activity not found")

        if activity in country.activities:
            return activity

        if activity not in country.activities:
            return None
