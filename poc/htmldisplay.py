#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Device, Domain, Mapping, Base

def create_session():
    engine = create_engine('sqlite:///iommu.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def holes():
    session = create_session()
    dev = session.query(Device).filter_by(last_attached=True).one()
    for m in session.query(Mapping).filter_by(device=dev).order_by(Mapping.phys_addr):
        should_next = "0x" + hex(int(m.phys_addr, 16) + int(m.size))[2:].zfill(16)
        found_next = session.query(Mapping).filter_by(device=dev, phys_addr=should_next).one_or_none()

        if found_next:
            print "{} {}".format(m.phys_addr, found_next.phys_addr)
        else:
            print "{} [[{}]]".format(m.phys_addr, should_next)

def main():
    draw_html()

def draw_html():
    ts = [20, 40, 10, 29]
    print "<style>"
    print "table {border: 1px black solid;}"
    print "td    {height: 20px; background: grey;}"

    for i,t in enumerate(ts):
        print "#td{} {{width: {}px;}}".format(i, t)

    print "</style>"
    
    print "<table><tr>"
    for i,t in enumerate(ts):
        print "<td id='td{}'>{}</td>".format(i, t)
    print "</tr></table>"

if __name__ == '__main__':
    main()
