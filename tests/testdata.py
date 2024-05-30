from src.model.agency import Agency
from src.database import Supervisor, TravelAgent, Customer, Country, Activity, db


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

def populate(agency: Agency):
    create_supervisors(agency)





