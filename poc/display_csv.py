#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export the current IOMMU mapping in a CSV file located in the out directory
"""
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
    Format is : mapping_id;iova;physical_address;size;device_bdf;device_name
    Device bdf and device name can be empty. """

    session = create_session()

    if not os.path.isdir('out'):
        os.makedirs('out')

    with open('out/iommu_config_display.csv', 'w') as output_csv:
        output_writer = csv.writer(output_csv, delimiter=';')

        # ---- Header
        output_writer.writerow(['MAPPING ID','IOVA','PHYSICAL ADDRESS', 'SIZE','DEVICE B.D:F', 'DEVICE NAME'])

        for map in session.query(Mapping).all():
            device = map.device

            if device is not None:
                device_name = device.name
                device_bdf = device.bdf
            else:
                device_name = ""
                device_bdf = ""

            output_writer.writerow([map.id, map.iova, map.phys_addr, map.size, device_bdf, device_name])


if __name__ == '__main__':
    main()
