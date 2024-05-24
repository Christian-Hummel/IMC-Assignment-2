from .travelAgent import TravelAgent

class Supervisor(TravelAgent):

    def __init__(self, employee_id: int, name: str, address: str, salary: float, nationality: str):
        super().__init__(employee_id,name,address,salary,nationality)