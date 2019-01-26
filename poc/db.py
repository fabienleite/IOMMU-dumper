#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from db_schema import Device, Mapping, Base
import re

import logging
logging.basicConfig(filename='db.log', level=logging.DEBUG)

class MapException(Exception):
    pass

def create_session():
    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def e_device(session, _name, _bdf, _lspci):
    m = re.findall('(?<=Memory at )(?:\w+)(?= \()', _lspci)
    existing_d = session.query(Device).filter_by(bdf=_bdf).one_or_none()

    if existing_d:
        logging.warning("Device {} already exist, not adding"
                .format(new_device.bdf))
        return existing_d
    else:
        new_device = Device(
                name = _name,
                bdf = _bdf,
                mapping = Mapping(
                    phys_addr = m[0] if m else "0x00000000",
                    iova = "0x0000000"
                )
        )
        session.add(new_device)
        session.commit()
        logging.info('Added device {} with base PA {}'
                .format(
                    new_device.bdf, 
                    new_device.mapping.phys_addr
                    ))
        return new_device


def e_map(session, _iova, _phys_addr, _size):
    existing_p = session.query(Mapping).filter_by(phys_addr=_phys_addr).one_or_none()
    existing_v = session.query(Mapping).filter_by(iova=_iova).one_or_none()

    new_mapping = Mapping(
            iova = _iova,
            phys_addr = _phys_addr,
            size = _size,
            )
    if not existing_v and not existing_p:
        session.add(new_mapping)
        session.commit()
        logging.info('Mapped v:{} p:{}'
                .format(
                    new_mapping.iova, 
                    new_mapping.phys_addr 
                    ))
        return new_mapping
    elif existing_v and existing_v.phys_addr != new_mapping.phys_addr:
        logging.info('(Update) PA <{}> => <{}> for VA {}'
                .format(
                    existing_v.phys_addr,
                    new_mapping.phys_addr,
                    existing_v.iova
                ))
        existing_v.phys_addr = new_mapping.phys_addr
        session.commit()
        return existing_v

    elif existing_p and existing_p.iova != new_mapping.iova:
        logging.info('(Update) VA <{}> => <{}> for PA {}'
                .format(
                    existing_p.iova,
                    new_mapping.iova,
                    existing_p.phys_addr
                    ))
        existing_p.iova = new_mapping.iova
        session.commit()
        return existing_p

def handle_event(session, event):
    if event['type'] == 'map':
        mapped = e_map(
                session,
                event['iova'],
                event['phys_addr'],
                event['size']
        )
        return mapped
    elif event['type'] == 'device':
        e_device(
                session,
                event['name'],
                event['bdf'],
                event['lspci']
                )


def create_db_from_parse():
    session = create_session()
    from event_parser import parse_tracefile

    #for e in parse_tracefile("/home/maxime/iommu_trace_wifi.txt"):
    for e in _retrieve_events():
        if '_debug' in e:
            logging.debug(e['_debug'])
        try:
            handle_event(session, e)
        except MapException as e:
            logging.warning(str(e), exc_info=False)
        except Exception as e:
            logging.error(str(e), exc_info=True)

    # Show mappings
    logging.debug('List of mappings')
    for m in session.query(Mapping).all():
        logging.debug('v:{} -> p:{} ({})'
                .format(m.iova, m.phys_addr, m.size))

def main():
    session = create_session()
    create_db_from_parse()

def _retrieve_events():
    return [
            {
                '_debug': 'a device with a mapping',
                'type': 'device',
                'name': 'GTX 960M',
                'bdf': '01:00.00',
                'lspci': "Memory at ee000000 (32-bit, non-prefetchable) [size=16M]"
            },
            { 
                '_debug': 'The mapping corresponding to previous attached dev',
                'type': 'map',
                'iova': '0x000faf',
                'size': 16384,
                'phys_addr': 'ee000000'
            },
            { 
                '_debug': 'a working map',
                'type': 'map',
                'iova': '0x000400',
                'size': 2048,
                'phys_addr': 'aa000fa'
            },
            { 
                '_debug': 'a working map',
                'type': 'map',
                'iova': '0x000600',
                'size': 2048,
                'phys_addr': 'bb000fa'
            },
            { 
                '_debug': 'a working map',
                'type': 'map',
                'iova': '0x000800',
                'size': 2048,
                'phys_addr': 'cc000fa'
            },
            { 
                '_debug': 'same iova than the working map, should update',
                'type': 'map',
                'iova': '0x000400',
                'size': 2048,
                'phys_addr': 'aa000fb'
            },
            { 
                '_debug': 'same phys_addr than working map, should update',
                'type': 'map',
                'iova': '0x000a00',
                'size': 2048,
                'phys_addr': 'bb000fa'
            },
    ]

if __name__ == '__main__':
    main()
