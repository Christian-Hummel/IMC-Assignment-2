from ..database import Supervisor, TravelAgent, Offer, Customer, Country, Activity, User, AgentStats, Message, db





class Agency(object):
    singleton_instance = None


    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance


# Supervisor

    def add_supervisor(self, new_supervisor: Supervisor):

        db.session.add(new_supervisor)
        db.session.commit()


    def register_user(self, new_user: User):

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

                        stats = db.session.query(AgentStats).filter_by(agent_id=agent_id).one_or_none()
                        if not stats:
                            stats = AgentStats(num_customers=1, agent_id=agent_id)
                            db.session.add(stats)
                        elif stats:
                            stats.num_customers += 1

                        db.session.commit()
                        return [agent,customer]
            elif customer.expert and agent.nationality != customer.preference:
                raise Exception("This TravelAgent does not have the required expert status")
            # customer does not require an expert and does not have any preferences
            elif not customer.expert and customer.preference == "None":
                for agent in supervisor.teammembers:
                    if agent.employee_id == employee_id:
                        customer.agent_id = employee_id

                        stats = db.session.query(AgentStats).filter_by(agent_id=agent_id).one_or_none()
                        if not stats:
                            stats = AgentStats(num_customers=1, agent_id=agent_id)
                            db.session.add(stats)
                        elif stats:
                            stats.num_customers += 1

                        db.session.commit()
                        return [agent,customer]
            # customer does not require an expert but has got a preference
            elif not customer.expert and customer.preference != "None":
                for agent in supervisor.teammembers:
                    if agent.employee_id == employee_id and customer.preference in [country.name for country in agent.countries]:
                        customer.agent_id = employee_id

                        stats = db.session.query(AgentStats).filter_by(agent_id=agent_id).one_or_none()
                        if not stats:
                            stats = AgentStats(num_customers=1, agent_id=agent_id)
                            db.session.add(stats)
                        elif stats:
                            stats.num_customers += 1

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

    def remove_agent(self,targeted_agent):

        employee_id = targeted_agent.employee_id

        if not targeted_agent.customers:
            db.session.query(TravelAgent).filter_by(employee_id=employee_id).delete()
            stats = db.session.query(AgentStats).filter_by(agent_id=employee_id).one_or_none()
            if stats:
                stats.delete()
            db.session.commit()
            return "removed"

        elif targeted_agent.customers:
            supervisor_id = targeted_agent.supervisor_id
            supervisor = db.session.query(Supervisor).filter_by(employee_id=supervisor_id).first()

            teammembers = [agent for agent in supervisor.teammembers if agent.employee_id != employee_id]

            for customer in targeted_agent.customers:
                for diffagent in teammembers:
                    for offer in customer.offers:
                        if customer.expert and customer.preference == diffagent.nationality:
                            if offer.country == diffagent.nationality and offer != "declined":
                                offer.agent_id = diffagent.employee_id
                            customer.agent_id = diffagent.employee_id
                            if diffagent.stats is None:
                                stats = AgentStats(num_customers=1, agent_id=diffagent.employee_id)
                                db.session.add(stats)
                            elif diffagent.stats is not None:
                                diffagent.stats.num_customers += 1

                        elif not customer.expert and customer.preference != "None" and customer.preference in [country.name for country in diffagent.countries]:
                            if offer.country in [country.name for country in diffagent.countries] and offer != "declined":
                                offer.agent_id = diffagent.employee_id
                            customer.agent_id = diffagent.employee_id
                            if diffagent.stats is None:
                                stats = AgentStats(num_customers=1, agent_id=diffagent.employee_id)
                                db.session.add(stats)
                            elif diffagent.stats is not None:
                                diffagent.stats.num_customers += 1

                        elif not customer.expert and customer.preference == "None":
                            if offer.country in [country.name for country in diffagent.countries] and offer != "declined":
                                offer.agent_id = diffagent.employee_id
                            customer.agent_id = diffagent.employee_id
                            if diffagent.stats is None:
                                stats = AgentStats(num_customers=1, agent_id=diffagent.employee_id)
                                db.session.add(stats)
                            elif diffagent.stats is not None:
                                diffagent.stats.num_customers += 1
                        else:
                            continue


        # check if there are offers that were not transferred (status declined excluded)
        offers = db.session.query(Offer).filter(Offer.agent_id==employee_id).filter(Offer.status!="declined").all()
        customers = db.session.query(Customer).filter_by(agent_id=employee_id).all()


        if not len(customers) and not len(offers):
            db.session.query(TravelAgent).filter_by(employee_id=employee_id).delete()
            db.session.commit()

            return "removed"
        else:
            return None


    def increase_agent_salary(self,supervisor_id,employee_id,increase):

        agent = db.session.query(TravelAgent).filter_by(employee_id=employee_id).first()

        supervisor = db.session.query(Supervisor).filter_by(employee_id=supervisor_id).first()



        if agent not in supervisor.teammembers:
            return None

        elif agent in supervisor.teammembers:

            request = db.session.query(Message).filter(Message.agent_id==employee_id).filter(Message.message=="raise").one_or_none()

            if request:

                stats = db.session.query(AgentStats).filter_by(agent_id=employee_id).one_or_none()

                if not stats:
                    raise Exception("This TravelAgent is not assigned to customers")

                if stats.total_revenue >= 5000:
                    agent.salary = agent.salary * (1 + increase)
                    db.session.query(Message).filter(Message.agent_id == employee_id).filter(Message.message == "raise").delete()
                    db.session.commit()
                    return agent
                else:
                    raise Exception("This TravelAgent is not allowed to have a raise in salary")

            elif not request:

                raise Exception("There is no request for a raise from this agent")

    def assign_country(self, country:Country, agent:TravelAgent, supervisor:Supervisor):

        if agent not in supervisor.teammembers:
            return None

        if country not in agent.countries:
            agent.countries.append(country)
            db.session.commit()
            return agent

        elif country in agent.countries:
            raise Exception("This country is already registered for this TravelAgent")

    def get_agent_stats(self,employee_id):

        stats = db.session.query(AgentStats).filter_by(agent_id=employee_id).one_or_none()

        if stats:
            return stats

        elif not stats:
            return None

    def discount_offer(self, agent: TravelAgent, offer: Offer, percentage):

        employee_id = agent.employee_id
        offer_id = offer.offer_id

        request = db.session.query(Message).filter(Message.agent_id==employee_id).filter(Message.offer_id==offer_id).one_or_none()

        if not request:
            raise Exception("There is no discount request for this offer")

        if percentage == 0:
            percentage = request.percentage

        offer.total_price = offer.total_price * (1-(percentage/100))
        offer.status = "changed"

        db.session.query(Message).filter(Message.agent_id==employee_id).filter(Message.offer_id==offer_id).delete()

        db.session.commit()
        return offer

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


    def request_raise(self, agent: TravelAgent):

        agent_id = agent.employee_id
        supervisor_id = agent.supervisor_id

        request = db.session.query(Message).filter(Message.agent_id==agent_id).filter(Message.message=="raise").one_or_none()

        if request:
            return None

        if not request:
            new_message = Message(supervisor_id=supervisor_id, agent_id=agent_id, message="raise")
            db.session.add(new_message)
            db.session.commit()
            return "A request for a raise in salary has been sent"

    def request_discount(self, agent: TravelAgent, offer: Offer, percentage):

        agent_id = agent.employee_id
        offer_id = offer.offer_id
        supervisor_id = agent.supervisor_id

        request = db.session.query(Message).filter_by(offer_id=offer_id).one_or_none()

        if request:
            return None

        new_message = Message(supervisor_id=supervisor_id,
                              agent_id=agent_id,
                              offer_id=offer_id,
                              percentage=percentage,
                              message="discount")
        db.session.add(new_message)
        db.session.commit()
        return f"A request for lowering the total price of Offer {offer_id} by {percentage} percent has been sent"

    def get_all_messages(self, supervisor_id):

        inbox = db.session.query(Message).filter_by(supervisor_id=supervisor_id).all()

        if len(inbox):
            return inbox
        elif not len(inbox):
            return None

# Customer

    def register_customer(self, new_customer: Customer):

        db.session.add(new_customer)
        db.session.commit()


    def request_expert(self, customer: Customer):

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

    def handle_offer(self, status, offer: Offer):

        if status == "accept":

            agent_id = offer.agent_id
            stats = db.session.query(AgentStats).filter_by(agent_id=agent_id).first()
            stats.num_trips += 1
            stats.total_revenue += offer.total_price
            offer.status = "accepted"
            db.session.commit()
            return offer


        elif status == "change":

            offer.status = "resend"
            db.session.commit()
            return offer

        elif status == "decline":

            offer.status = "declined"
            db.session.commit()
            return offer



# Country

    def add_country(self, new_country: Country):

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

    def get_country_stats(self, country: Country):

        country_name = country.name

        offers = db.session.query(Offer).filter(Offer.country==country.name).filter(Offer.status=="accepted").all()


        if not len(offers):
            return None
        elif len(offers):

            stats = {
                "country": country_name,
                "visits": 0,
                "total_revenue": 0,

            }
            activities_dict = {}

            for offer in offers:
                stats["visits"] += 1
                stats["total_revenue"] += offer.total_price
                for activity in offer.activities:
                    if activity.name not in activities_dict:
                        activities_dict[activity.name] = 1
                    elif activity.name in activities_dict:
                        activities_dict[activity.name] += 1

            favourite = [key for key,value in activities_dict.items() if value == max(activities_dict.values())]

            if len(favourite) == 1:
                stats["favourite_activity"] = favourite
            else:
                stats["favourite_activities"] = favourite

            return stats






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


    def remove_activity(self, country: Country, r_activity:Activity):

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
