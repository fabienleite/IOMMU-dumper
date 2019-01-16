from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Mapping, Base


def create_session():
    """ Create a session to retrieved data from iommu.db.
    Return the database session object. """

    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def main ():
    """ Display each mapping on the terminal.
    Display IOVA, physical address and the size."""

    session = create_session()

    # Defining header and separators
    beginning_and_end = "-" * 54
    first_line = " MAPPING |  IOVA            | PHYSICAL ADDRESS | SIZE "

    print(beginning_and_end + "\n" + first_line + "\n" + beginning_and_end)

    for cnt, m in enumerate(session.query(Mapping).all(), 1):

        #device = session.query(Device).filter_by(mapping=map).one_or_none()

        #iova = [m.iova for m in session.query(Mapping).filter_by(device=d).all()]
        #phys_addr = [m.phys_addr for m in session.query(Mapping).filter_by(device=d).all()]
        #
        # biggest_len = (
        #     len(iova)
        #     if len(iova) > len(phys_addr)
        #     else len(phys_addr)
        # )
        # biggest_len_is_virt = (
        #     True if len(iova) > len(phys_addr) else False
        # )
        #
        # for i in range(0, biggest_len):
        #     beginning = " " + str(cnt) + "      | " + d.bdf + " | "
        #     if i > 0:
        #         beginning = " _      | " + "_         | "
        #
        #     try:
        #         print(beginning + iova[i] + " | " + phys_addr[i])
        #     except IndexError:
        #         if biggest_len_is_virt:
        #             print(beginning + iova + " | " + "_         ")
        #         else:
        #             print(beginning + "_         " + " | " + phys_addr[i])

        iova = str(m.iova)
        pa = str(m.phys_addr)
        size = str(m.size)

        print(" " + str(cnt) + "       | " + iova + " | " + pa + " | " + size)

        print(beginning_and_end)


if __name__ == '__main__':
    main()
