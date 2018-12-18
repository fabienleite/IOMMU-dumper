from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Device, Mapping, Base
import csv

def create_session():
    """ Create a session to retrieved data from iommu.db.
    Return the database session object. """

    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def main ():
    """ Output mapping in a CSV file.
    Format is : device_name, b.d:f, iova, physical_address """

    session = create_session()

    with open('out/iommu_output.csv', 'w') as output_csv:
        output_writer = csv.writer(output_csv, delimiter=';')

        # Header
        # A adapter suivant la nouvelle bdd
        output_writer.writerow(['IOVA','Physical adress'])

        # for cnt, d in enumerate(session.query(Device).all(), 1):
        #     name = d.name
        #     bdf = d.bdf
        #     iova = [m.iova for m in session.query(Mapping).all()]
        #     phys_addr = [m.phys_addr for m in session.query(Mapping).all()]

        # A adapter suivant la nouvelle bdd
        for map in session.query(Mapping).all():

            output_writer.writerow([map.iova, map.phys_addr])

            # une ligne pour chaque mapping : iova, phys_addr

            # output_csv.writerow(name, bdf, iova[i], phys_addr[i])


if __name__ == '__main__':
    main()
