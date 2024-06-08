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



# TravelAgent


# Customer

    def register_customer(self, new_customer:Customer):

        db.session.add(new_customer)
        db.session.commit()

# Country

    def add_country(self, new_country:Country):

        db.session.add(new_country)
        db.session.commit()


    def get_all_countries(self):

        countries = db.session.query(Country).order_by(Country.name).all()

        if countries:
            return countries
        elif len(countries) == 0:
            raise Exception("There are no countries registered")


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

        country = db.session.query(Country).filter_by(country_id=country_id).first()

        for activity in country.activities:
            if activity.activity_id == updated_activity.activity_id:
                activity.name = updated_activity.name
                activity.price = updated_activity.price
                db.session.commit()