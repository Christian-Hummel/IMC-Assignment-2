from typing import List, Union, Optional

#from .travelAgent import TravelAgent
#from .supervisor import Supervisor
#from .customer import Customer
#from .country import Country
#from .activity import Activity


from ..database import Employee, Customer, Country, Activity, db





class Agency(object):
    singleton_instance = None


    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance



    def add_supervisor(self, new_supervisor:Employee):

        db.session.add(new_supervisor)
        db.session.commit()
