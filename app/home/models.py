#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

from sqlalchemy import Column, Integer, String, DateTime

from app import db

logger = logging.getLogger(__name__)


class Announcement(db.Model):
    __tablename__ = "announcement"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32))
    url = Column(String(255))
    type = Column(Integer, default=1)
    createtime = Column(DateTime())
    updatetime = Column(DateTime())

    def __repr__(self):
        return {"id": self.id, "title": self.title, "url": self.url, "type": self.type}


class Announcement_detail(db.Model):
    __tablename__ = "announcement_detail"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32))
    announcement_id = Column(Integer, primary_key=True)
    data = Column(String(2000))


class Announcement_read(db.Model):
    __tablename__ = "announcement_read"

    id = Column(Integer, primary_key=True, autoincrement=True)
    announcement_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)
    createtime = Column(DateTime())
