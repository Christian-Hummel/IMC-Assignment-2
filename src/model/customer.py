

class Customer(object):

    def __init__(self,customer_id: int, name: str, address: str, email: str, budget: float, preference: str, expert: bool):
        self.customer_id = customer_id,
        self.name = name,
        self.address = address,
        self.email = email,
        self.budget = budget,
        self.preference = preference
        self.expert = expert
