#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Device, Mapping, Base
import csv, os

def create_session():
    """ Create a session to retrieved data from iommu.db.
    Return the database session object. """

    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def main():
    """ Output existing mappings in a CSV file named iommu_config_display.csv
    and located in the out directory.
    Format is : iova;physical_address;size;device_name (can be empty) """

    session = create_session()

    if not os.path.isdir('out'):
        os.makedirs('out')

    with open('out/iommu_config_display.csv', 'w') as output_csv:
        output_writer = csv.writer(output_csv, delimiter=';')

        # ---- Header
        output_writer.writerow(['MAPPING','IOVA','PHYSICAL ADDRESS', 'SIZE','DEVICE B.D:F', 'DEVICE NAME'])

        for map in session.query(Mapping).all():
            device = session.query(Device).filter_by(mapping=map).one_or_none()

            if device is not None:
                device_name = device.name
                device_bdf = device.bdf
            else:
                device_name = ""
                device_bdf = ""

            output_writer.writerow([map.id, map.iova, map.phys_addr, map.size, device_bdf, device_name])


if __name__ == '__main__':
    main()
