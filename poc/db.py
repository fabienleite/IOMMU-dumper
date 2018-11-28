#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_schema import Device, Domain, Mapping, Base

def main():
    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    new_domain = Domain(name='host')
    new_device = Device(name='03:0000.01', domain=new_domain)
    new_mapping = Mapping(  iova='0x00ff',
                            phys_addr='0x5000',
                            size=2048,
                            device=new_device)
    session.add(new_domain)
    session.add(new_device)
    session.add(new_mapping)
    session.commit()

    for mapping in session.query(Mapping).all():
        print mapping.__dict__


if __name__ == '__main__':
    main()
