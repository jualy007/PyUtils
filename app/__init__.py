#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import logging.config
import os
import time
from importlib import import_module

import yaml
from flask import Flask, url_for
from sqlalchemy import event
from sqlalchemy.engine import Engine

from .encrypt import Encrypt
from .extensions import (
    cache,
    csrf,
    db,
    mail,
    whooshee,
    mongo,
    gravatar,
    moment,
    login_manager,
    celery,
)

__version__ = "1.0.1"

logger = logging.getLogger(__name__)


def create_app(config=None):
    application = Flask(__name__, static_folder="base/static")

    configure_app(application, config)

    configure_extensions(application)

    register_blueprint(application)

    configure_database(application)

    apply_themes(application)

    return application


def configure_app(app, config):
    app.config.from_object(config)

    # Setting up logging as early as possible
    configure_logging(app)


def register_blueprint(app):
    for module_name in (
            "base",
            "forms",
            "ui",
            "home",
            "tables",
            "data",
            "additional",
            "base",
            "tools",
    ):
        module = import_module("app.{}.routes".format(module_name))
        app.register_blueprint(module.blueprint)


def configure_celery_app(app, celery):
    """Configures the celery app."""
    app.config.update({"BROKER_URL": app.config["CELERY_BROKER_URL"]})
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


def configure_extensions(app):
    """Configures the extensions."""

    # Flask-WTF CSRF
    csrf.init_app(app)

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Mail
    mail.init_app(app)

    # Flask-Cache
    cache.init_app(app)

    # Flask-Whooshee
    whooshee.init_app(app)

    # Flask-Gravatar
    gravatar.init_app(app)

    # Flask-Moment
    moment.init_app(app)

    # Flask-PyMongo
    mongo.init_app(app)

    # Flask-Login
    login_manager.init_app(app)


def configure_logging(app):
    """Configures logging."""
    if app.config.get("USE_DEFAULT_LOGGING"):
        configure_default_logging(app)
    else:
        file = app.config.get("LOG_CONF_FILE")
        if file is not None:
            # Update Log File Name
            with open(file, "r") as fhandle:
                configs = yaml.load(fhandle)
                configs["handlers"]["info_file_handler"]["filename"] = os.path.join(
                    app.config.get("LOG_PATH"), "info.log"
                )
                configs["handlers"]["error_file_handler"]["filename"] = os.path.join(
                    app.config.get("LOG_PATH"), "errors.log"
                )
                configs["handlers"]["DashBoard"]["filename"] = os.path.join(
                    app.config.get("LOG_PATH"), "DashBoard.log"
                )
                logging.config.dictConfig(configs)

    if app.config["SQLALCHEMY_ECHO"]:
        # Ref: http://stackoverflow.com/a/8428546
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(
                conn, cursor, statement, parameters, context, executemany
        ):
            conn.info.setdefault("query_start_time", []).append(time.time())

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(
                conn, cursor, statement, parameters, context, executemany
        ):
            total = time.time() - conn.info["query_start_time"].pop(-1)
            app.logger.debug("Total Time: %f", total)


def configure_default_logging(app):
    # Load default logging config
    logging.config.dictConfig(app.config["LOG_DEFAULT_CONF"])

    if app.config["SEND_LOGS"]:
        configure_mail_logs(app)


def configure_mail_logs(app):
    from logging.handlers import SMTPHandler

    formatter = logging.Formatter("%(asctime)s %(levelname)-7s %(name)-25s %(message)s")
    mail_handler = SMTPHandler(
        app.config["MAIL_SERVER"],
        app.config["MAIL_DEFAULT_SENDER"],
        app.config["ADMINS"],
        "application error, no admins specified",
        (
            app.config["MAIL_USERNAME"],
            Encrypt(app.config["SECRET_KEY"]).decrypt(app.config["MAIL_PASSWORD"]),
        ),
    )

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(formatter)
    app.logger.addHandler(mail_handler)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def apply_themes(app):
    """
    Add support for themes.

    If DEFAULT_THEME is set then all calls to
      url_for('static', filename='')
      will modfify the url to include the theme name

    The theme parameter can be set directly in url_for as well:
      ex. url_for('static', filename='', theme='')

    If the file cannot be found in the /static/<theme>/ lcation then
      the url will not be modified and the file is expected to be
      in the default /static/ location
    """

    @app.context_processor
    def override_url_for():
        return dict(url_for=_generate_url_for_theme)

    def _generate_url_for_theme(endpoint, **values):
        if endpoint.endswith("static"):
            themename = values.get("theme", None) or app.config.get(
                "DEFAULT_THEME", None
            )
            if themename:
                theme_file = "{}/{}".format(themename, values.get("filename", ""))
                if os.path.isfile(os.path.join(app.static_folder, theme_file)):
                    values["filename"] = theme_file
        return url_for(endpoint, **values)
