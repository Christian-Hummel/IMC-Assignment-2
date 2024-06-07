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
                "activities": country.activity
            }

            return country_json
        elif not country:
            return None


# Activity