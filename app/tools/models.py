#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

from sqlalchemy import Column, Integer, String

from app import db

logger = logging.getLogger(__name__)


class Software(db.Model):
    __tablename__ = "software"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), primary_key=True)
    description = Column(String(255))
    url = Column(String(255))
    download_url = Column(String(255))
    download_count = Column(Integer, default=0)
    comment = Column(Integer)
    tag = Column(String(32))
