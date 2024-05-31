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



# TravelAgent


# Customer


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

        country_json = {
            "country_id": country.country_id,
            "name": country.name,
            "activities": country.activity
        }

        if country:
            return country_json
        elif not country:
            return None


# Activity