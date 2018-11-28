#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from db_schema import Device, Domain, Mapping, Base

import json # for pretty printing dicts
import logging
logging.basicConfig(filename='db.log', level=logging.DEBUG)

def create_session():
    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

"""
{ 
    bdf: '0001:2b.01',
    event_type: 'map',
    iova: '0x000400',
    size: 2048
    phys_addr: '0xff000fa'
}
{ 
    event_type: 'unmap',
    iova: '0x000400',
    size: 2048
}
{ 
    bdf: '0001:2b.01',
    device_name: 'SATA controller: Intel Corporation Sunrise Point-LP SATA Controller [AHCI mode] (rev 21)'
    event_type: 'attach'
}
"""
# Cannot create a device with map() event !! only with attach
# Cannot attach a device if it is already attached to domain

def _retrieve_events():
    return [
            {
                'device_bdf': '0001:2b.01',
                'device_name': 'SATA controller',
                'event_type': 'attach'
            },
            { 
                'event_type': 'map',
                'iova': '0x000400',
                'size': 2048,
                'phys_addr': '0xff000fa'
            }
            ]


def add_domain(session, domain_name):
    exists = session.query(Domain).filter_by(name=domain_name).one_or_none()
    if not exists:
        session.add(Domain(name=domain_name))
        session.commit()
        logging.info('Domain {} added'.format(domain_name))
    else:
        logging.info('Domain {} already exists, not adding'.format(domain_name))

def add_device(session, event):
    """event is a dict"""
    # search for event['device_bdf'] in table device
    exists = session.query(Device).filter_by(bdf=event['device_bdf']).one_or_none()
    if not exists:
        session.add(
                Device(
                    name = event['device_name'],
                    bdf  = event['device_bdf'],
                    domain = session.query(Domain).filter_by(name='host').one()
                    )
            )
        session.commit()
        logging.info('Device {} added'.format(event['device_bdf']))
    else:
        logging.info('Device {} already exists, not adding'.format(event['device_bdf']))


def main():
    session = create_session()
    add_domain(session, 'host')

    for event in _retrieve_events():
        if event['event_type'] == 'attach':
            add_device(session, event)





"""

    new_device = Device(
                    name   = trace['bdf'],
                    domain = new_domain
    )

    new_mapping = Mapping(
                        iova      = trace['iova'],
                        phys_addr = trace['phys_addr'],
                        size      = trace['size'],
                        device    = new_device
    )
    session.add(new_domain)
    session.add(new_device)
    session.add(new_mapping)
    session.commit()

    for mapping in session.query(Mapping).all():
        _mapping = mapping.__dict__
        del _mapping['_sa_instance_state']
        print json.dumps(_mapping, sort_keys=True)
"""

if __name__ == '__main__':
    main()
