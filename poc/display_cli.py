#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Mapping, Base, Device


def create_session():
    """ Create a session to retrieved data from iommu.db.
    Return the database session object. """

    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def main ():
    """ Display each mapping on the terminal.
    Display IOVA, physical address, size and, if a device is attached, its bdf and name."""

    session = create_session()

    # Defining header and separators
    beginning_and_end = "-" * 80
    first_line = " MAPPING | IOVA             | PHYSICAL ADDRESS | SIZE | B.D:F    | DEVICE NAME "

    print(beginning_and_end + "\n" + first_line + "\n" + beginning_and_end)

    for cnt, m in enumerate(session.query(Mapping).all(), 1):
        iova = str(m.iova)
        pa = str(m.phys_addr)
        size = str(m.size)

        device = session.query(Device).filter_by(mapping=m).one_or_none()

        if device is not None:
            d_bdf = str(device.bdf)
            d_name = str(device.name)
        else:
            d_bdf = "        "
            d_name = ""

        print(" " + str(cnt) + "       | " + iova + " | " + pa + " | " + size + " | " + d_bdf + " | " + d_name)

        print(beginning_and_end)


if __name__ == '__main__':
    main()
