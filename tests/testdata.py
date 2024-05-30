from src.model.agency import Agency
from src.database import Supervisor, TravelAgent, Customer, Country, Activity, User, db


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


def create_agents(agency: Agency):
    travel_agents = [
        TravelAgent(employee_id=240, name="Christopher Lee", address="Arlington Boulevard 9, 3829 Chicago",
                    email="Christopher.Lee@hammertrips.com", salary=3500, role="travelAgent", nationality="UK",
                    supervisor_id=23),
        TravelAgent(employee_id=245, name="Philipp Lienhart", address="Brauhausgasse 38, 3829 Freiburg",
                    email="Philipp.Lienhart@hammertrips.com", salary=3900, role="travelAgent", nationality="Austria",
                    supervisor_id=34),
        TravelAgent(employee_id=250, name="John Doe", address="Main Street 5, 1234 Springfield",
                    email="John.Doe@hammertrips.com", salary=3100, role="travelAgent", nationality="USA",
                    supervisor_id=45),
        TravelAgent(employee_id=255, name="Jane Smith", address="Elm Street 12, 5678 Gotham",
                    email="Jane.Smith@hammertrips.com", salary=3200, role="travelAgent", nationality="Canada",
                    supervisor_id=56),
        TravelAgent(employee_id=260, name="Robert Brown", address="Oak Avenue 22, 9101 Metropolis",
                    email="Robert.Brown@hammertrips.com", salary=3400, role="travelAgent", nationality="Australia",
                    supervisor_id=67),
        TravelAgent(employee_id=265, name="Emily Davis", address="Pine Lane 34, 1121 Smallville",
                    email="Emily.Davis@hammertrips.com", salary=3300, role="travelAgent", nationality="Germany",
                    supervisor_id=78),
        TravelAgent(employee_id=270, name="Michael Johnson", address="Maple Road 45, 3141 Star City",
                    email="Michael.Johnson@hammertrips.com", salary=3500, role="travelAgent", nationality="France",
                    supervisor_id=89),
        TravelAgent(employee_id=275, name="Sarah Wilson", address="Birch Boulevard 56, 5161 Central City",
                    email="Sarah.Wilson@hammertrips.com", salary=3200, role="travelAgent", nationality="Italy",
                    supervisor_id=91),
        TravelAgent(employee_id=280, name="David Miller", address="Cedar Drive 67, 7181 Coast City",
                    email="David.Miller@hammertrips.com", salary=3700, role="travelAgent", nationality="Spain",
                    supervisor_id=102),
        TravelAgent(employee_id=285, name="Emma Taylor", address="Willow Way 78, 9201 Bludhaven",
                    email="Emma.Taylor@hammertrips.com", salary=3600, role="travelAgent", nationality="Japan",
                    supervisor_id=113),
        TravelAgent(employee_id=290, name="James Anderson", address="Aspen Avenue 89, 1122 Atlantis",
                    email="James.Anderson@hammertrips.com", salary=3300, role="travelAgent", nationality="China",
                    supervisor_id=124),
        TravelAgent(employee_id=295, name="Olivia Thomas", address="Cypress Street 90, 3344 Wakanda",
                    email="Olivia.Thomas@hammertrips.com", salary=3500, role="travelAgent", nationality="India",
                    supervisor_id=135),
        TravelAgent(employee_id=300, name="William Martinez", address="Redwood Lane 101, 5566 Asgard",
                    email="William.Martinez@hammertrips.com", salary=3700, role="travelAgent", nationality="Brazil",
                    supervisor_id=146),
        TravelAgent(employee_id=305, name="Isabella Moore", address="Juniper Drive 112, 7788 Themyscira",
                    email="Isabella.Moore@hammertrips.com", salary=3400, role="travelAgent", nationality="Mexico",
                    supervisor_id=157),
        TravelAgent(employee_id=310, name="Benjamin Harris", address="Olive Road 123, 9900 Nanda Parbat",
                    email="Benjamin.Harris@hammertrips.com", salary=3600, role="travelAgent",
                    nationality="South Africa", supervisor_id=168),
        TravelAgent(employee_id=315, name="Sophia Clark", address="Spruce Street 134, 1112 Korugar",
                    email="Sophia.Clark@hammertrips.com", salary=3700, role="travelAgent", nationality="Russia",
                    supervisor_id=179),
        TravelAgent(employee_id=320, name="Matthew Lewis", address="Chestnut Avenue 145, 3334 K'un-Lun",
                    email="Matthew.Lewis@hammertrips.com", salary=3300, role="travelAgent", nationality="Netherlands",
                    supervisor_id=190),
        TravelAgent(employee_id=325, name="Charlotte Walker", address="Hickory Lane 156, 5556 Madripoor",
                    email="Charlotte.Walker@hammertrips.com", salary=3100, role="travelAgent", nationality="Sweden",
                    supervisor_id=201),
        TravelAgent(employee_id=330, name="Elijah Young", address="Poplar Boulevard 167, 7778 Attilan",
                    email="Elijah.Young@hammertrips.com", salary=3900, role="travelAgent", nationality="Norway",
                    supervisor_id=23),
        TravelAgent(employee_id=335, name="Amelia King", address="Alder Drive 178, 9990 Genosha",
                    email="Amelia.King@hammertrips.com", salary=3400, role="travelAgent", nationality="Denmark",
                    supervisor_id=34)
    ]

    db.session.add_all(travel_agents)
    db.session.commit()
def populate(agency: Agency):
    create_supervisors(agency)
    create_users(agency)
    create_agents(agency)





