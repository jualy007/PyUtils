#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from app import db, login_manager
from app.encrypt import Encrypt

logger = logging.getLogger(__name__)

users_roles = db.Table(
    "users_roles",
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("user_id", Integer(), ForeignKey("user.id")),
    Column("role_id", Integer(), ForeignKey("role.id")),
)


class Role(db.Model):
    __tablename__ = "role"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    rolename = Column(String(80), unique=True)
    active = Column(Boolean(), default=True)
    description = Column(String(255))
    createtime = Column(DateTime())
    updatetime = Column(DateTime())

    def __repr__(self):
        return str(self.rolename)

    def isactive(self):
        return self.active


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean(), default=True)
    createtime = Column(DateTime())
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(16))
    current_login_ip = Column(String(16))
    login_count = Column(Integer, default=0)
    roles = db.relationship(
        "Role", secondary=users_roles, backref=db.backref("users", lazy="dynamic")
    )

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            if property == "password":
                value = Encrypt.hashpw(value)
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def is_active(self):
        return self.active

    def roles(self):
        return self.roles


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    return user if user else None
