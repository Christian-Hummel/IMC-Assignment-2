from src.model.agency import Agency
from src.database import Supervisor, TravelAgent, Offer, Customer, Country, Activity, User, db


def create_supervisors(agency: Agency):
    supervisors = [
        Supervisor(employee_id=13, name="Harry Styles", address="123 Elm Street, Springfield",
                   email="Harry.Styles@hammertrips.com", salary=20145, nationality="USA", role="supervisor"),
        Supervisor(employee_id=23, name="Emma Watson", address="456 Oak Avenue, Gotham",
                   email="Emma.Watson@hammertrips.com", salary=22035, nationality="UK", role="supervisor"),
        Supervisor(employee_id=34, name="Chris Evans", address="789 Pine Lane, Metropolis",
                   email="Chris.Evans@hammertrips.com", salary=25987, nationality="USA", role="supervisor"),
        Supervisor(employee_id=45, name="Scarlett Johansson", address="101 Maple Road, Smallville",
                   email="Scarlett.Johansson@hammertrips.com", salary=18234, nationality="USA", role="supervisor"),
        Supervisor(employee_id=56, name="Tom Holland", address="202 Birch Boulevard, Star City",
                   email="Tom.Holland@hammertrips.com", salary=27450, nationality="UK", role="supervisor"),
        Supervisor(employee_id=67, name="Gal Gadot", address="303 Cedar Drive, Central City",
                   email="Gal.Gadot@hammertrips.com", salary=21590, nationality="Israel", role="supervisor"),
        Supervisor(employee_id=78, name="Robert Downey Jr.", address="404 Willow Way, Coast City",
                   email="Robert.Downey@hammertrips.com", salary=28945, nationality="USA", role="supervisor"),
        Supervisor(employee_id=89, name="Jennifer Lawrence", address="505 Aspen Avenue, Bludhaven",
                   email="Jennifer.Lawrence@hammertrips.com", salary=23250, nationality="USA", role="supervisor"),
        Supervisor(employee_id=91, name="Ryan Reynolds", address="606 Cypress Street, Atlantis",
                   email="Ryan.Reynolds@hammertrips.com", salary=24890, nationality="Canada", role="supervisor"),
        Supervisor(employee_id=102, name="Natalie Portman", address="707 Redwood Lane, Wakanda",
                   email="Natalie.Portman@hammertrips.com", salary=26980, nationality="USA", role="supervisor"),
        Supervisor(employee_id=113, name="Benedict Cumberbatch", address="808 Juniper Drive, Asgard",
                   email="Benedict.Cumberbatch@hammertrips.com", salary=22345, nationality="UK", role="supervisor"),
        Supervisor(employee_id=124, name="Anne Hathaway", address="909 Olive Road, Themyscira",
                   email="Anne.Hathaway@hammertrips.com", salary=19450, nationality="USA", role="supervisor"),
        Supervisor(employee_id=135, name="Mark Ruffalo", address="111 Spruce Street, Nanda Parbat",
                   email="Mark.Ruffalo@hammertrips.com", salary=28700, nationality="USA", role="supervisor"),
        Supervisor(employee_id=146, name="Margot Robbie", address="222 Chestnut Avenue, Korugar",
                   email="Margot.Robbie@hammertrips.com", salary=21360, nationality="Australia", role="supervisor"),
        Supervisor(employee_id=157, name="Hugh Jackman", address="333 Hickory Lane, K'un-Lun",
                   email="Hugh.Jackman@hammertrips.com", salary=29150, nationality="Australia", role="supervisor"),
        Supervisor(employee_id=168, name="Emily Blunt", address="444 Poplar Boulevard, Madripoor",
                   email="Emily.Blunt@hammertrips.com", salary=22840, nationality="UK", role="supervisor"),
        Supervisor(employee_id=179, name="Chris Hemsworth", address="555 Alder Drive, Attilan",
                   email="Chris.Hemsworth@hammertrips.com", salary=25370, nationality="Australia", role="supervisor"),
        Supervisor(employee_id=190, name="Zoe Saldana", address="666 Fir Street, Genosha",
                   email="Zoe.Saldana@hammertrips.com", salary=27550, nationality="USA", role="supervisor"),
        Supervisor(employee_id=201, name="Tom Hiddleston", address="777 Magnolia Avenue, Latveria",
                   email="Tom.Hiddleston@hammertrips.com", salary=21985, nationality="UK", role="supervisor"),
        Supervisor(employee_id=212, name="Karen Gillan", address="888 Walnut Lane, Oa",
                   email="Karen.Gillan@hammertrips.com", salary=23975, nationality="UK", role="supervisor")
    ]

    # add Supervisors to fixture
    db.session.add_all(supervisors)
    db.session.commit()


def create_users(agency: Agency):
    users = [
        User(id=1, username="Harry", password_hash="4k5@Jz!r8pQs#7Hd", manager_id=12),
        User(id=2, username="Emma", password_hash="B7d#2lPw!3Qh@z8M", manager_id=23),
        User(id=3, username="Chris", password_hash="z&3Kf$9Qh4Pw@8Jn", manager_id=34),
        User(id=4, username="Scarlett", password_hash="U1m#8zLp@5Fs$6Th", manager_id=45),
        User(id=5, username="Tom", password_hash="R2j$7Ls!8Fw@9Mv#", manager_id=56),
        User(id=6, username="Gal", password_hash="V3c#6Kd$8Qs!1Pf@", manager_id=67),
        User(id=7, username="Robert", password_hash="X5n@4Pw$9Lf!2Zr#", manager_id=78),
        User(id=8, username="Jennifer", password_hash="A6q$7Zr!3Mw@9Lf#", manager_id=89),
        User(id=9, username="Ryan", password_hash="D8s#2Lq$5Mw!1Nv@", manager_id=91),
        User(id=10, username="Natalie", password_hash="F4n!3Mv$7Qh@9Kr#", manager_id=102),
        User(id=11, username="Benedict", password_hash="G5k#8Zr$4Lq!1Pw@", manager_id=113),
        User(id=12, username="Anne", password_hash="J6m@9Pw$3Lf!2Kr#", manager_id=124),
        User(id=13, username="Mark", password_hash="L2p$4Jr!8Mv@5Qs#", manager_id=135),
        User(id=14, username="Margot", password_hash="N3k#7Zr$1Lq!9Pw@", manager_id=146),
        User(id=15, username="Hugh", password_hash="Q8s!2Pw$6Lf#3Jr@", manager_id=157),
        User(id=16, username="Emily", password_hash="T4m@1Kr$9Qh!7Lz#", manager_id=168),
        User(id=17, username="Christian", password_hash="Y5c#8Mv$3Lf!1Jr@", manager_id=179),
        User(id=18, username="Zoe", password_hash="Z2p$6Qh!4Ls@9Kr#", manager_id=190)
    ]

    db.session.add_all(users)
    db.session.commit()


def create_countries(agency: Agency):
    countries = [
        Country(country_id=901,name="Germany"),
        Country(country_id=902, name="France"),
        Country(country_id=903, name="England"),
        Country(country_id=904, name="Scotland"),
        Country(country_id=905, name="Poland"),
        Country(country_id=906, name="Czech Republic"),
        Country(country_id=907, name="Japan"),
        Country(country_id=908, name="Canada"),
        Country(country_id=909, name="Senegal"),
        Country(country_id=910, name="Chile"),
        Country(country_id=911, name="Brazil"),
        Country(country_id=912, name="Lativa"),
        Country(country_id=913, name="Spain"),
        Country(country_id=914, name="Finland"),
        Country(country_id=915, name="Denmark"),
        Country(country_id=916, name="Norway"),
        Country(country_id=917, name="Sweden"),
        Country(country_id=918, name="Slovenia"),
        Country(country_id=919, name="Netherlands"),
        Country(country_id=920, name="Simbabwe"),
    ]

    db.session.add_all(countries)
    db.session.commit()

def create_agents(agency: Agency):
    agent1 = TravelAgent(employee_id=240, name="Christopher Lee", address="Arlington Boulevard 9, 3829 Chicago",
                    email="Christopher.Lee@hammertrips.com", salary=3500, role="travelAgent", nationality="UK",
                    supervisor_id=23)


    agent2 =  TravelAgent(employee_id=245, name="Philipp Lienhart", address="Brauhausgasse 38, 3829 Freiburg",
                    email="Philipp.Lienhart@hammertrips.com", salary=3900, role="travelAgent", nationality="Austria",
                    supervisor_id=34)


    agent3 = TravelAgent(employee_id=250, name="John Doe", address="Main Street 5, 1234 Springfield",
                    email="John.Doe@hammertrips.com", salary=3100, role="travelAgent", nationality="USA",
                    supervisor_id=45)


    agent4 = TravelAgent(employee_id=255, name="Jane Smith", address="Elm Street 12, 5678 Gotham",
                    email="Jane.Smith@hammertrips.com", salary=3200, role="travelAgent", nationality="Canada",
                    supervisor_id=56)



    agent5 = TravelAgent(employee_id=260, name="Robert Brown", address="Oak Avenue 22, 9101 Metropolis",
                    email="Robert.Brown@hammertrips.com", salary=3400, role="travelAgent", nationality="Australia",
                    supervisor_id=67)


    agent6 = TravelAgent(employee_id=265, name="Emily Davis", address="Pine Lane 34, 1121 Smallville",
                    email="Emily.Davis@hammertrips.com", salary=3300, role="travelAgent", nationality="Germany",
                    supervisor_id=78)



    agent7 = TravelAgent(employee_id=270, name="Michael Johnson", address="Maple Road 45, 3141 Star City",
                    email="Michael.Johnson@hammertrips.com", salary=3500, role="travelAgent", nationality="France",
                    supervisor_id=89)



    agent8 = TravelAgent(employee_id=275, name="Sarah Wilson", address="Birch Boulevard 56, 5161 Central City",
                    email="Sarah.Wilson@hammertrips.com", salary=3200, role="travelAgent", nationality="Italy",
                    supervisor_id=91)


    agent9 =  TravelAgent(employee_id=280, name="David Miller", address="Cedar Drive 67, 7181 Coast City",
                    email="David.Miller@hammertrips.com", salary=3700, role="travelAgent", nationality="Spain",
                    supervisor_id=102)



    agent10 = TravelAgent(employee_id=285, name="Emma Taylor", address="Willow Way 78, 9201 Bludhaven",
                    email="Emma.Taylor@hammertrips.com", salary=3600, role="travelAgent", nationality="Japan",
                    supervisor_id=113)


    agent11 = TravelAgent(employee_id=290, name="James Anderson", address="Aspen Avenue 89, 1122 Atlantis",
                    email="James.Anderson@hammertrips.com", salary=3300, role="travelAgent", nationality="China",
                    supervisor_id=124)



    agent12 = TravelAgent(employee_id=295, name="Olivia Thomas", address="Cypress Street 90, 3344 Wakanda",
                    email="Olivia.Thomas@hammertrips.com", salary=3500, role="travelAgent", nationality="India",
                    supervisor_id=135)


    agent13 = TravelAgent(employee_id=300, name="William Martinez", address="Redwood Lane 101, 5566 Asgard",
                    email="William.Martinez@hammertrips.com", salary=3700, role="travelAgent", nationality="Brazil",
                    supervisor_id=146)



    agent14 = TravelAgent(employee_id=305, name="Isabella Moore", address="Juniper Drive 112, 7788 Themyscira",
                    email="Isabella.Moore@hammertrips.com", salary=3400, role="travelAgent", nationality="Mexico",
                    supervisor_id=157)



    agent15 = TravelAgent(employee_id=310, name="Benjamin Harris", address="Olive Road 123, 9900 Nanda Parbat",
                    email="Benjamin.Harris@hammertrips.com", salary=3600, role="travelAgent",
                    nationality="South Africa", supervisor_id=168)



    agent16 =  TravelAgent(employee_id=315, name="Sophia Clark", address="Spruce Street 134, 1112 Korugar",
                    email="Sophia.Clark@hammertrips.com", salary=3700, role="travelAgent", nationality="Finland",
                    supervisor_id=179)



    agent17 =  TravelAgent(employee_id=320, name="Matthew Lewis", address="Chestnut Avenue 145, 3334 K'un-Lun",
                    email="Matthew.Lewis@hammertrips.com", salary=3300, role="travelAgent", nationality="Netherlands",
                    supervisor_id=190)



    agent18 = TravelAgent(employee_id=325, name="Charlotte Walker", address="Hickory Lane 156, 5556 Madripoor",
                    email="Charlotte.Walker@hammertrips.com", salary=3100, role="travelAgent", nationality="Sweden",
                    supervisor_id=201)



    agent19 = TravelAgent(employee_id=330, name="Elijah Young", address="Poplar Boulevard 167, 7778 Attilan",
                    email="Elijah.Young@hammertrips.com", salary=3900, role="travelAgent", nationality="Norway",
                    supervisor_id=23)



    agent20 = TravelAgent(employee_id=335, name="Amelia King", address="Alder Drive 178, 9990 Genosha",
                    email="Amelia.King@hammertrips.com", salary=3400, role="travelAgent", nationality="Denmark",
                    supervisor_id=34)


    country1 = db.session.query(Country).filter_by(country_id=901).first()
    country2 = db.session.query(Country).filter_by(country_id=902).first()
    country3 = db.session.query(Country).filter_by(country_id=903).first()
    country4 = db.session.query(Country).filter_by(country_id=904).first()
    country5 = db.session.query(Country).filter_by(country_id=905).first()
    country6 = db.session.query(Country).filter_by(country_id=906).first()
    country7 = db.session.query(Country).filter_by(country_id=907).first()
    country8 = db.session.query(Country).filter_by(country_id=908).first()
    country9 = db.session.query(Country).filter_by(country_id=909).first()
    country10 = db.session.query(Country).filter_by(country_id=910).first()
    country11 = db.session.query(Country).filter_by(country_id=911).first()
    country12 = db.session.query(Country).filter_by(country_id=912).first()
    country13 = db.session.query(Country).filter_by(country_id=913).first()



    agent1.countries.append(country1)
    agent2.countries.extend([country1,country2])
    agent3.countries.extend([country1,country3])
    agent4.countries.extend([country1,country2,country4])
    agent5.countries.extend([country1,country5])
    agent6.countries.extend([country1,country6])
    agent7.countries.extend([country1,country7])
    agent8.countries.extend([country1,country8])
    agent9.countries.extend([country1,country9])
    agent10.countries.extend([country1,country10])
    agent11.countries.extend([country1,country11])
    agent12.countries.extend([country1,country12])
    agent13.countries.extend([country1,country13])
    agent14.countries.extend([country1,country4,country7])



    db.session.add_all([agent1,agent2,agent3,agent4,agent5,agent6,agent7,agent8,agent9,agent10,agent11,agent12,agent13,agent14,agent15,agent16,agent17,agent18,agent19,agent20])
    db.session.commit()



def create_customers(agency: Agency):
    customers = [
        Customer(customer_id=701, name="Stephen Hawking", address="Richard's Street 32, 4728 Oxford",
                 email="Stephen@hawking.co.uk", budget=20000, preference="Austria", expert=False, agent_id=240),
        Customer(customer_id=702, name="Nuri Sahin", address="Borsingplatz 4, 2732 Dortmund", email="Nuri.Sahin@bvb.de",
                 budget=15000, preference="None", expert=False, agent_id=245),
        Customer(customer_id=703, name="Ada Lovelace", address="Ada Street 42, 1878 London",
                 email="Ada.Lovelace@maths.com", budget=25000, preference="UK", expert=True, agent_id=250),
        Customer(customer_id=704, name="Nikola Tesla", address="Electric Avenue 8, 1130 New York",
                 email="Nikola.Tesla@genius.com", budget=18000, preference="Germany", expert=True, agent_id=255),
        Customer(customer_id=705, name="Marie Curie", address="Science Road 23, 7516 Paris",
                 email="Marie.Curie@radioactive.fr", budget=22000, preference="France", expert=True, agent_id=260),
        Customer(customer_id=706, name="Albert Einstein", address="Relativity Blvd 9, 1000 Berlin",
                 email="Albert.Einstein@theory.de", budget=30000, preference="Germany", expert=True, agent_id=265),
        Customer(customer_id=707, name="Isaac Newton", address="Gravity Lane 10, 1200 Cambridge",
                 email="Isaac.Newton@physics.uk", budget=27000, preference="None", expert=True, agent_id=270),
        Customer(customer_id=708, name="Galileo Galilei", address="Stars Way 14, 6012 Pisa",
                 email="Galileo.Galilei@astronomy.it", budget=24000, preference="Italy", expert=True, agent_id=275),
        Customer(customer_id=709, name="Leonardo da Vinci", address="Art Street 55, 5012 Florence",
                 email="Leonardo.DaVinci@renaissance.it", budget=26000, preference="Italy", expert=True, agent_id=280),
        Customer(customer_id=710, name="Charles Darwin", address="Evolution Blvd 8, 2099 London",
                 email="Charles.Darwin@biology.uk", budget=21000, preference="UK", expert=True, agent_id=285),
        Customer(customer_id=711, name="Michael Faraday", address="Magnetism Street 12, 1871 London",
                 email="Michael.Faraday@electricity.uk", budget=22000, preference="None", expert=True, agent_id=290),
        Customer(customer_id=712, name="Thomas Edison", address="Inventor's Alley 19, 7310 New Jersey",
                 email="Thomas.Edison@invention.us", budget=25000, preference="USA", expert=False, agent_id=295),
        Customer(customer_id=713, name="Sigmund Freud", address="Mind Way 6, 1010 Vienna",
                 email="Sigmund.Freud@psychology.at", budget=23000, preference="Austria", expert=False, agent_id=300),
        Customer(customer_id=714, name="Gregor Mendel", address="Genetics Blvd 22, 6120 Brno",
                 email="Gregor.Mendel@biology.cz", budget=28000, preference="None", expert=False, agent_id=305),
        Customer(customer_id=715, name="Louis Pasteur", address="Bacteriology Street 17, 7505 Paris",
                 email="Louis.Pasteur@microbiology.fr", budget=29000, preference="France", expert=True, agent_id=310),
        Customer(customer_id=716, name="Jane Goodall", address="Primate Alley 21, 9012 Nairobi",
                 email="Jane.Goodall@anthropology.ke", budget=20000, preference="None", expert=True, agent_id=315),
        Customer(customer_id=717, name="Rosalind Franklin", address="DNA Lane 33, 1012 London",
                 email="Rosalind.Franklin@genetics.uk", budget=26000, preference="None", expert=False, agent_id=0),
        Customer(customer_id=718, name="James Watt", address="Steam Road 9, 8015 Glasgow",
                 email="James.Watt@engineering.uk", budget=22000, preference="UK", expert=True, agent_id=325),
        Customer(customer_id=719, name="Alfred Nobel", address="Mining Road 5, 1120 Stockholm",
                 email="Alfred.Nobel@chemistry.se", budget=27000, preference="France", expert=False, agent_id=0),
        Customer(customer_id=720, name="Marie Tharp", address="Ocean Avenue 4, 1001 New York",
                 email="Marie.Tharp@geology.us", budget=21000, preference="Austria", expert=True, agent_id=0)
    ]

    db.session.add_all(customers)
    db.session.commit()



def create_activities(agency: Agency):


    activity1 = Activity(activity_id=601, name="Miniatur Wunderland", price=20)
    activity2 = Activity(activity_id=602, name="Chateau des ducs de Bretagne", price=30)
    activity3 = Activity(activity_id=603, name="London Eye", price=50)
    activity4 = Activity(activity_id=604, name="Edingburgh Castle", price=25)
    activity5 = Activity(activity_id=605, name="Malbork Castle", price=22)
    activity6 = Activity(activity_id=606, name="Pub Crawl", price=50)
    activity7 = Activity(activity_id=607, name="Baseball Game", price=60)
    activity8 = Activity(activity_id=608, name="Calgary Stampede", price=40)
    activity9 = Activity(activity_id=609, name="Safari", price=100)
    activity10 = Activity(activity_id=610, name="Rapa Nui", price=50)
    activity11 = Activity(activity_id=611, name="Stadion Tour", price=70)
    activity12 = Activity(activity_id=612, name="Ruandales pils", price=20)
    activity13 = Activity(activity_id=613, name="Sagrada Familia", price=26)
    activity14 = Activity(activity_id=614, name="City Tour", price=50)
    activity15 = Activity(activity_id=615, name="Horseriding", price=30)


    country1 = db.session.query(Country).filter_by(country_id=901).first()
    country2 = db.session.query(Country).filter_by(country_id=902).first()
    country3 = db.session.query(Country).filter_by(country_id=903).first()
    country4 = db.session.query(Country).filter_by(country_id=904).first()
    country5 = db.session.query(Country).filter_by(country_id=905).first()
    country6 = db.session.query(Country).filter_by(country_id=906).first()
    country7 = db.session.query(Country).filter_by(country_id=907).first()
    country8 = db.session.query(Country).filter_by(country_id=908).first()
    country9 = db.session.query(Country).filter_by(country_id=909).first()
    country10 = db.session.query(Country).filter_by(country_id=910).first()
    country11 = db.session.query(Country).filter_by(country_id=911).first()
    country12 = db.session.query(Country).filter_by(country_id=912).first()
    country13 = db.session.query(Country).filter_by(country_id=913).first()
    country14 = db.session.query(Country).filter_by(country_id=914).first()

    country1.activities.extend([activity1, activity11, activity15])
    country2.activities.extend([activity2, activity11])
    country3.activities.extend([activity3, activity15])
    country4.activities.extend([activity4, activity15])
    country5.activities.extend([activity5, activity15])
    country6.activities.extend([activity6, activity15])
    country7.activities.extend([activity7, activity15])
    country8.activities.extend([activity8, activity15])
    country9.activities.extend([activity9, activity15])
    country10.activities.extend([activity10,activity15])
    country11.activities.extend([activity11,activity15])
    country12.activities.extend([activity12, activity15])
    country13.activities.extend([activity13, activity15])
    country14.activities.extend([activity14, activity15])



    db.session.add_all([country1,country2,country3,country4,country5,country6,country7,country8,country9,country10,country11,country12,country13,country14])
    db.session.commit()

def create_offers(agency: Agency):
    activity1 = db.session.query(Activity).filter_by(activity_id=601).first()
    activity2 = db.session.query(Activity).filter_by(activity_id=602).first()
    activity3 = db.session.query(Activity).filter_by(activity_id=603).first()
    activity4 = db.session.query(Activity).filter_by(activity_id=604).first()
    activity5 = db.session.query(Activity).filter_by(activity_id=605).first()
    activity6 = db.session.query(Activity).filter_by(activity_id=606).first()
    activity7 = db.session.query(Activity).filter_by(activity_id=607).first()
    activity8 = db.session.query(Activity).filter_by(activity_id=608).first()
    activity9 = db.session.query(Activity).filter_by(activity_id=609).first()
    activity10 = db.session.query(Activity).filter_by(activity_id=610).first()
    activity11 = db.session.query(Activity).filter_by(activity_id=611).first()
    activity12 = db.session.query(Activity).filter_by(activity_id=612).first()
    activity13 = db.session.query(Activity).filter_by(activity_id=613).first()
    activity14 = db.session.query(Activity).filter_by(activity_id=614).first()
    activity15 = db.session.query(Activity).filter_by(activity_id=615).first()



    offer1 = Offer(offer_id=801, country="Germany", total_price=6000, status="pending", agent_id=255, customer_id=704)
    offer2 = Offer(offer_id=802, country="France", total_price=200, status="resend", agent_id=270, customer_id=707)
    offer3 = Offer(offer_id=803, country="England", total_price=350, status="changed", agent_id=275, customer_id=708)
    offer4 = Offer(offer_id=804, country="Scotland", total_price=500, status="pending", agent_id=280, customer_id=709)
    offer5 = Offer(offer_id=805, country="Poland", total_price=22, status="resend", agent_id=260, customer_id=705)
    offer6 = Offer(offer_id=806, country="Senegal", total_price=300, status="changed", agent_id=290, customer_id=711)
    offer7 = Offer(offer_id=807, country="Czech Republic", total_price=350, status="pending", agent_id=295, customer_id=712)
    offer8 = Offer(offer_id=808, country="Canada", total_price=400, status="pending", agent_id=300, customer_id=713)
    offer9 = Offer(offer_id=809, country="Lativa", total_price=600, status="pending", agent_id=305, customer_id=714)
    offer10 = Offer(offer_id=810, country="Spain", total_price=800, status="pending", agent_id=310, customer_id=715)
    offer11 = Offer(offer_id=811, country="Brazil", total_price=1000, status="budget", agent_id=315, customer_id=716)
    offer12 = Offer(offer_id=812, country="Finland", total_price=2000, status="declined", agent_id=265, customer_id=706)

    offer1.activities.extend([activity1, activity11])
    offer2.activities.extend([activity2, activity15])
    offer3.activities.extend([activity3, activity15])
    offer4.activities.extend([activity4])
    offer5.activities.extend([activity5])
    offer6.activities.extend([activity9])
    offer7.activities.extend([activity6, activity15])
    offer8.activities.extend([activity8])
    offer9.activities.extend([activity12])
    offer10.activities.extend([activity13])
    offer11.activities.extend([activity11])
    offer12.activities.extend([activity14])


    db.session.add_all([offer1, offer2, offer3, offer4, offer5, offer6, offer7, offer8, offer9, offer10, offer11, offer12])
    db.session.commit()


def populate(agency: Agency):
    create_supervisors(agency)
    create_users(agency)
    create_countries(agency)
    create_agents(agency)
    create_customers(agency)
    create_activities(agency)
    create_offers(agency)




