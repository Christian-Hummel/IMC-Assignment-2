
# Add instructions how to run the program in the final README and check requirements.txt 

# API for a travelling agency

I want to program an Application for customers and Employers of a travelling agency, in order to be able to book a trip to a certain country with a set of activities. Once a customer registers, he will be forwarded to a travel agent, who makes recommendation and is in charge of managing the trip. Every travel agent has got a agent supervisor on his side, who can be seen as a manager.

It will support a database, personal information about customers and employers, as well as data regarding the offered countries can be stored inside. It is also possible to include networking features, like a "manager login" to be able to use functionality that normal agents can not, or sending requests between travel agents and their supervisors. 

**Manager Login**

The idea is that you log in with certain credentials and you can execute certain commands that will function like routes in swagger, but I do not know if it would be even possible to integrate a server-client structure to the swagger interface or to make it work with flask-restx.

But the basic idea is that travel agents can send requests, e.g. raise in salary, and the manager can either confirm or deny it, depending on set conditions.

**Management of Travel Agents**

A travel agent is able to manage a trip for a customer. He or she should essentially help the customer to get the best out of their journey regarding their budget. A travel agent has got a unique employee ID, a name, an email address, an address, a salary and a nationality that also defines their country of special expertise. Each travel agent has a list of customers that they are assigned to and a list of Countries, for which they can present offers.

**Management of Supervisors**

A supervisor is in charge of management tasks to enable the travel agents to concentrate on their jobs in the Front Office. He assigns travel agents to customers, is able to raise their salary as well as releasing them from the agency. Furthermore he can confirm discounts for the total price of a trip. Each Supervisor has a unique employee ID, a name, an email address, an address, a salary and a nationality. Each Supervisor has a list of travel agents who they are responsible for. 

**Management of Customers**

Each customer has to register to be able to plan and book a trip with a travel agent supporting them. Each customer has got a unique customer ID, a name, an email address, an address, a budget and a country which they want to visit. Each customer can have a special preference for a specific country and ask for the services of a travel agent with expert status for a specific country.

**Management of Countries**

A country represents the desired destination of a Customer. Each country is connected to one or more activities. A country has got a unique country_ID a name and a list of activities. Each activity has got an activity id which does not necessarily need to be unique, a name and a price.


## external libraries

- flask
- flask-restx
- flask-sqlalchemy
- swagger
- sqlite3
- threadings



### Functions

**Customer**

register() - adds a customer to the agency - c

book_trip() - accepting the offer from the agent, a booked trip will be counted as visited for stats -- combined with -- cancel_trip() - reject an offer from the travel agent - c

request_expert() - require an travel agent with expert status for country specified in preferences - c

show_offers() - show all valid offers (status "pending" or "changed") for this customer - c


**TravelAgent**

present_offer() - sends a possible trip recommendation to the customer, it cannot exceed the budget in terms of total price and a customer can receive multiple different offers from his travelAgent - c

request_raise() - send a request to the respective supervisor to get an increase in salary

update_agent() - allows to update following attributes: name, email, address - c


**Country**

add_country() - registers a country to be used for trip plans by the agents - c

get_country_by_id() - displays country attributes: country_ID, name and all current activities - c

get_all_countries() - shows a list of all countries - c

get_country_stats() - displays the number of total visits, the most popular activity and the total revenue it generated - c


**Activity**

add_activity() - connects an activity to a country - c

update_activity() - enables to change the name and the price of an activity - c

delete_activity() - removes an activity from the agency - c

get_activity_by_id() - displays attributes of an activity: activity_id, name, price - c



**Supervisor**

get_customer_by_id() - display attributes from customer: customer_id, name, email, address, budget, preference, expert, TravelAgent_id - c

get_all_customers() - show a list of all customers - c

assign_agent() - assigns an agent to counsel a customer - c

add_agent() - introduces a new travel agent to the agency under his supervision - adds the supervisor attribute to this class - c

raise_salary() - increases the salary for a specific travel agent - c

delete_agent() - removes an agent from the agency, all his customers will be transferred to one of his colleagues, if he is the only one left, he cannot be fired. - c

set_discount() - lowers the price for the total price of an offer by a set percentage

get_agent_stats() - shows the number of customers, the total revenue he produced and the amount of trips he sold - c

get_agent_by_id() - displays travel agent attributes: employer_ID, name, email, address, salary, nationality, supervisor_id - c

show_all_agents() - displays information about all agents he or she supervises: employer_ID, name, email, address, salary, nationality, - c

get_supervisor_by_id() - displays supervisor attributes: employer_ID, name, email, address, salary, nationality and number of travel agents under his supervision - c

assign_country() - registers a travel agent to a specific country, such that he can make offers for it - c


#### Notes

the travel agent supervisor interaction with raise salary could made with certain constraints, for example it will only be increased if this agent has got at least 5 successful deals with a specific amount of revenue in total.

the salary of each travel agent can be set to a default value, the same holds for supervisors, but their default value will be higher, naturally.

Employee ID might be convenient because of inheritance, but I do not see a problem with this variable name, in most businesses the higher ups do also have the same type of ID number like everyone else.
