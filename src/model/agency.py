from typing import List, Union, Optional


from .supervisor import Supervisor


from ..database import Employee, db





class Agency(object):
    singleton_instance = None


    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance



    def add_supervisor(self, new_supervisor:Supervisor):
        supervisor = Employee(employee_id = new_supervisor.employee_id,
                              name= new_supervisor.name,
                              address=new_supervisor.address,
                              email=new_supervisor.email,
                              salary=new_supervisor.salary,
                              nationality=new_supervisor.nationality,
                              role="supervisor"
                              )

        db.session.add(supervisor)
        db.session.commit()
