#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from db_schema import Device, Domain, Mapping, Base
from db import create_session

def get_all_mappings(session):
    """
    Get all mappings object into a SQLAlchemy DB

    Input :
        - A SQLAlchemy DB session

    Output :
        - A list of Mapping objects
    """
    return session.query(Mapping).order_by(Mapping.phys_addr)

def calc_hole(first_map, second_map, min_size=419430400):
    """
    Calcul hole between 2 mappings.

    format of a Mapping Tuple:
        2 integers :
            - physical_address
            - mapping_size
        formated as following
        ( physical_address, mapping_size )

    Input :
        - first_map : a Mapping Tuple
        - second_map : a Mapping Tuple
        - min_size : an Integer representing the minimum wanted size. By default 50MB

    Output :
        - A Mapping Tuple or None (if there is no hole)
    """
    hole_start = int(first_map[0],16) + first_map[1] #The end of first mapping
    hole_size = int(second_map[0],16) - hole_start

    if hole_size>min_size:
        return ( hex(hole_start), hole_size )

    else :
        return None


def calc_all_holes(type, value):
    """
    Calcul all holes between mappings.

    Input :
        - Type (session or dataset) of the second input
        - A SQLAlchemy DB session or a dataset (list of mappings)

    Output :
        - A list of Mapping Tuple (See calc_hole description)
    """

    if type == 'session':
        mappings = list(get_all_mappings(session))
    else:
        mappings = value

    holes_list = []

    for i in range(1,len(mappings)):
        first_mapping = mappings[i-1]
        second_mapping = mappings[i]

        first_tuple = (first_mapping.phys_addr, first_mapping.size)
        second_tuple = (second_mapping.phys_addr, second_mapping.size)

        hole = calc_hole(first_tuple, second_tuple)

        if hole != None:
            holes_list.append(hole)
    return holes_list


if __name__=="__main__":
    session=create_session()

    print(calc_all_holes('session', session))

    data = list(get_all_mappings(session))
    print(calc_all_holes('dataset', data))
