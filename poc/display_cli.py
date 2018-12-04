from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Device, Mapping, Base


def create_session():
    """ Create a session to retrieved data from iommu.db.
    Return the database session object. """

    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def main ():
    """ Display mapping for each device on the terminal.
    Display device name, device B:D.F, virtual and physical address(es)."""

    session = create_session()

    # Defining header and separators
    beginning_and_end = "-" * 54
    first_line = " Device | BDF       | VA         | PA"

    print(beginning_and_end + "\n" + first_line + "\n" + beginning_and_end)

    for cnt, d in enumerate(session.query(Device).all(), 1):

        print(d.name)

        iova = [m.iova for m in session.query(Mapping).filter_by(device=d).all()]
        phys_addr = [m.phys_addr for m in session.query(Mapping).filter_by(device=d).all()]

        biggest_len = (
            len(iova)
            if len(iova) > len(phys_addr)
            else len(phys_addr)
        )
        biggest_len_is_virt = (
            True if len(iova) > len(phys_addr) else False
        )

        for i in range(0, biggest_len):
            beginning = " " + str(cnt) + "      | " + d.bdf + " | "
            if i > 0:
                beginning = " _      | " + "_         | "

            try:
                print(beginning + iova[i] + " | " + phys_addr[i])
            except IndexError:
                if biggest_len_is_virt:
                    print(beginning + iova + " | " + "_         ")
                else:
                    print(beginning + "_         " + " | " + phys_addr[i])

        print(beginning_and_end)


if __name__ == '__main__':
    main()
