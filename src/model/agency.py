from typing import List, Union, Optional


from ..database import Supervisor, TravelAgent, Customer, Country, Activity, User, db





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

        db.session.add(new_agent)
        db.session.commit()


    def show_all_agents(self,supervisor_id):

        supervisor = db.session.query(Supervisor).filter_by(employee_id=supervisor_id).first()

        if hasattr(supervisor, "teammembers"):
            team = supervisor.teammembers

            return team
        else:
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

# TravelAgent


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