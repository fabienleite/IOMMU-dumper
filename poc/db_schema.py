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

class Mapping(Base):
    __tablename__ = 'mapping'
    id            = Column(Integer, primary_key=True)
    iova          = Column(String(255))
    phys_addr     = Column(String(255))
    size          = Column(Integer)
    device_id     = Column(Integer, ForeignKey('device.id'))
    device        = relationship('Device', backref='mapping')

engine = create_engine('sqlite:///iommu.db')
Base.metadata.create_all(engine)
