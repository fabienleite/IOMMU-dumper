#!/bin/false
# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Domain(Base):
    __tablename__ = 'domain'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    domain_id = Column(Integer, ForeignKey('domain.id'))
    domain = relationship('Domain', backref='device')

class Mapping(Base):
    __tablename__ = 'mapping'
    id = Column(Integer, primary_key=True)
    devices_id = Column(Integer, ForeignKey('device.id'))
    iova = Column(String(255))
    phys_addr = Column(String(255))
    size = Column(Integer)
    device = relationship('Device', backref='mapping')

engine = create_engine('sqlite:///iommu.db')
Base.metadata.create_all(engine)
