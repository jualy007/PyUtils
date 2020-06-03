#!/usr/bin/python
# -*- coding:utf-8 -*-

from celery import Celery
from flask_caching import Cache
from flask_gravatar import Gravatar
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from flask_wtf.csrf import CSRFProtect

# Database
db = SQLAlchemy()

# Whooshee (Full Text Search)
whooshee = Whooshee()

# Mail
mail = Mail()

# Caching
cache = Cache()

# Mongo
mongo = PyMongo()

# CSRF
csrf = CSRFProtect()

# Celery
celery = Celery("app")

# Gravatar
gravatar = Gravatar()

# Moment
moment = Moment()

# Login
login_manager = LoginManager()
