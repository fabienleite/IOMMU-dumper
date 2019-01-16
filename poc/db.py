#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from db_schema import Device, Domain, Mapping, Base

import logging
logging.basicConfig(filename='db.log', level=logging.DEBUG)

class MapException(Exception):
    pass

def create_session():
    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def e_map(session, _iova, _phys_addr, _size):
    existing_p = session.query(Mapping).filter_by(phys_addr=_phys_addr).one_or_none()
    existing_v = session.query(Mapping).filter_by(iova=_iova).one_or_none()

    if not existing_v and not existing_p:
        new_mapping = Mapping(
                iova = _iova,
                phys_addr = _phys_addr,
                size = _size,
                )
        session.add(new_mapping)
        session.commit()
        logging.info('Mapped v:{} p:{}'
                .format(
                    new_mapping.iova, 
                    new_mapping.phys_addr 
                    ))
        return new_mapping
    elif existing_v:
        raise MapException('Virtual address {} is already mapped to physical address {}'
                .format(
                    existing_v.iova,
                    existing_v.phys_addr,
                ))
    elif existing_p:
        raise MapException('Physical address {} is already mapped to virtual address {}'
                .format(
                    existing_p.phys_addr,
                    existing_p.iova
                    ))

def handle_event(session, event):
    mapped = e_map(
            session,
            event['iova'],
            event['phys_addr'],
            event['size']
    )
    return mapped

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
                '_debug': 'a working map',
                'iova': '0x000600',
                'size': 2048,
                'phys_addr': '0xaa000fa'
            },
            { 
                '_debug': 'a working map',
                'iova': '0x000400',
                'size': 2048,
                'phys_addr': '0xff000fa'
            },
            { 
                '_debug': 'a working map',
                'iova': '0x000408',
                'size': 2048,
                'phys_addr': '0xff000ff'
            },
            { 
                '_debug': 'same iova than the working map, should fail',
                'iova': '0x000400',
                'size': 2048,
                'phys_addr': '0xff000fb'
            },
            { 
                '_debug': 'same phys_addr than working map, should fail',
                'iova': '0x000404',
                'size': 2048,
                'phys_addr': '0xff000fa'
            },
    ]

if __name__ == '__main__':
    main()
