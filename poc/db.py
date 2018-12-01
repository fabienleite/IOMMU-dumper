#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from db_schema import Device, Domain, Mapping, Base

import json # for pretty printing dicts
import logging
logging.basicConfig(filename='db.log', level=logging.DEBUG)

class MapException(Exception):
    pass

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



def add_domain(session, domain_name):
    exists = session.query(Domain).filter_by(name=domain_name).one_or_none()
    if not exists:
        session.add(Domain(name=domain_name))
        session.commit()
        logging.info('Domain {} added'.format(domain_name))
    else:
        logging.info('Domain {} already exists, not adding'.format(domain_name))

def e_attach(session, _name, _bdf):
    """
        Adds device to database and attach to domain host
        If device already exist, do nothing
        In all cases, return orm object for the actual device
    """
    # bdf is unique
    existing = session.query(Device).filter_by(bdf=_bdf).one_or_none()
    if not existing:
        new_device = Device(
                name = _name,
                bdf  = _bdf,
                domain = session.query(Domain).filter_by(name='host').one()
                )
        session.add(new_device)
        session.commit()
        logging.info('Device {} added'.format(new_device.bdf))
        return new_device
    else:
        logging.info('Device {} already exists, not adding'.format(existing.bdf))
        return existing

def e_map(session, _device, _iova, _phys_addr, _size):
    """
        Adds mapping entry and return orm object
    # iova is unique for each device
    # phys_addr is unique
        if already mapped (highly improbable), raise an ugly Exception()
    """
    existing_p = session.query(Mapping).filter_by(phys_addr=_phys_addr).one_or_none()
    existing_v = session.query(Mapping).filter_by(iova=_iova, device=_device).one_or_none()

    if not existing_v and not existing_p:
        new_mapping = Mapping(
                iova = _iova,
                phys_addr = _phys_addr,
                size = _size,
                device = _device
                )
        session.add(new_mapping)
        session.commit()
        logging.info('Mapped v:{} p:{} for device {}'
                .format(
                    new_mapping.iova, 
                    new_mapping.phys_addr, 
                    new_mapping.device.bdf
                    ))
        return new_mapping

    elif existing_v:
        raise MapException('Virtual address {} is already mapped to physical address {} for device {}'
                .format(
                    existing_v.iova,
                    existing_v.phys_addr,
                    existing_v.device.bdf
                ))
    elif existing_p:
        raise MapException('Physical address {} is already mapped to device {}'
                .format(
                    existing_p.phys_addr,
                    existing_p.device.bdf
                    ))

def handle_event(session, event):
    last_attached = session.query(Device).order_by(Device.id.desc()).first()

    # TODO il faut trouver un moyen de récupérer la dernier device attached
    #if last_attached:
    #    logging.debug('Last attached device is {}'.format(last_attached.bdf))

    if event['event_type'] == 'attach':
        attached = e_attach(
                session,
                event['dev_name'],
                event['dev_bdf']
        )
    elif event['event_type'] == 'map':
        mapped = e_map(
                session,
                last_attached,
                event['iova'],
                event['phys_addr'],
                event['size']
        )

def main():
    session = create_session()
    add_domain(session, 'host')

    for e in _retrieve_events():
        if '_debug' in e:
            logging.debug(e['_debug'])
        try:
            handle_event(session, e)
        except MapException as e:
            logging.warning(e.message, exc_info=False)
        except Exception as e:
            logging.error(e.message, exc_info=True)

    # Show devices
    #logging.debug("Device list: {}".format( [(d.name, d.bdf) for d in session.query(Device).all()] ))

    # Show mappings
    logging.debug('List of mappings')
    for m in session.query(Mapping).all():
        logging.debug('{} v:{} -> p:{} ({})'
                .format(m.device.bdf, m.iova, m.phys_addr, m.size))

def _retrieve_events():
    return [
            {
                'dev_bdf': '1111:2b.01',
                'dev_name': 'USB controller',
                'event_type': 'attach'
            },
            { 
                '_debug': 'a working map',
                'event_type': 'map',
                'iova': '0x000400',
                'size': 2048,
                'phys_addr': '0xff000fa'
            },
            { 
                '_debug': 'same iova and device than the working map, should fail',
                'event_type': 'map',
                'iova': '0x000400',
                'size': 2048,
                'phys_addr': '0xff000fb'
            },
            {
                'dev_bdf': '2222:2b.01',
                'dev_name': 'SATA controller',
                'event_type': 'attach'
            },
            { 
                '_debug': 'same iova than working map but different device, should work',
                'event_type': 'map',
                'iova': '0x000400',
                'size': 2048,
                'phys_addr': '0xff000fc'
            },
            { 
                '_debug': 'same phys_addr than working map, shoud fail',
                'event_type': 'map',
                'iova': '0x000404',
                'size': 2048,
                'phys_addr': '0xff000fa'
            },
    ]

if __name__ == '__main__':
    main()
