#!/bin/false
# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Device(Base):
    __tablename__ = 'device'
    id            = Column(Integer, primary_key=True)
    name          = Column(String(255), unique=True)
    bdf           = Column(String(255), unique=True)

class DevMem(Base):
    __tablename__ = 'devmem'
    id            = Column(Integer, primary_key=True)
    device_id     = Column(Integer, ForeignKey('device.id'))
    device        = relationship('Device', backref='devmem')
    mapping_id    = Column(Integer, ForeignKey('mapping.id'))
    mapping       = relationship('Mapping', backref='devmem')


class Mapping(Base):
    __tablename__ = 'mapping'
    id            = Column(Integer, primary_key=True)
    iova          = Column(String(255), unique=True)
    phys_addr     = Column(String(255), unique=True)
    size          = Column(Integer)

engine = create_engine('sqlite:///iommu.db')
Base.metadata.create_all(engine)
