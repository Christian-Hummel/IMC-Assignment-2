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


    def get_countries(self):

        countries = db.session.query(Country).order_by(Country.name).all()

        if countries:
            return countries

        else:
            return None

# Activity