#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
from datetime import datetime

import jwt
from flask import flash, redirect, url_for, render_template, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import or_

from app import db
from app.base import blueprint
from app.base.forms import (
    LoginForm,
    CreateAccountForm,
    ForgetPasswdForm,
)
from app.base.models import User, Role
from app.encrypt import Encrypt
from configs.config import Config

logger = logging.getLogger(__name__)


@blueprint.route("/")
def route_default():
    return redirect(url_for("base_blueprint.login"))


@blueprint.route("/<template>")
@login_required
def route_template(template):
    return render_template(template + ".html")


@blueprint.route("/fixed_<template>")
@login_required
def route_fixed_template(template):
    return render_template("fixed/fixed_{}.html".format(template))


@blueprint.route("/page_<error>")
def route_errors(error):
    return render_template("errors/page_{}.html".format(error))


## Login & Registration


@blueprint.route("/auth", methods=["GET"])
def auth():
    return jsonify(
        jwt.encode(
            {
                "exp": datetime.utcnow()
                       + datetime.timedelta(days=1, hours=0, minutes=0, seconds=0),
                "iat": datetime.datetime.utcnow(),
            },
            Config.SECRET_KEY,
        )
    )


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_ip = request.remote_addr
    login_form = LoginForm(request.form)

    if request.method == "GET":
        if current_user.is_authenticated:
            user = current_user
            user.current_login_at, user.current_login_ip, user.login_count = (
                datetime.utcnow(),
                login_ip,
                user.login_count + 1,
            )
            db.session.commit()
            return redirect(url_for("home_blueprint.index"))
        else:
            return render_template("login/login.html", login_form=login_form)
    else:
        if login_form.validate_on_submit():
            user = User.query.filter(
                or_(
                    User.username == request.form.get("username"),
                    User.email == request.form.get("username"),
                )
            ).first()

            if (
                    user
                    and user.is_active()
                    and Encrypt.checkpw(request.form.get("password"), user.password)
            ):
                login_user(user)
                return redirect(url_for("base_blueprint.route_default"))
            return render_template("errors/page_403.html")


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    create_account_form = CreateAccountForm(request.form)

    if request.method == "GET":
        return render_template(
            "login/register.html", create_account_form=create_account_form
        )
    else:
        if create_account_form.validate_on_submit():
            rf = request.form

            user = User.query.filter(
                or_(User.username == rf.get("username"), User.email == rf.get("email"))
            ).first()

            if user:
                flash("User Exist")
            else:
                role = Role(rolename="noruser").query.get(1)

                user = User(
                    username=rf.get("username"),
                    email=rf.get("email"),
                    password=rf.get("password"),
                    active=True,
                    createtime=datetime.utcnow(),
                )

                role.users = [user]
                db.session.add(user)
                db.session.commit()
                flash("Register Success")
        else:
            logger.error(create_account_form.errors)

        return redirect(url_for("base_blueprint.login"))


@blueprint.route("/forgetpassword", methods=["GET", "POST"])
def forget():
    form = ForgetPasswdForm()

    if request.method == "GET":
        return render_template("")
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(User.email == request.form.get("email")).first()

            if user is not None:
                # send code via email
                return redirect()


@blueprint.route("/reset_password")
def reset(token):
    redirect(url_for("/home"))


@blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user


@blueprint.route("/logout")
@login_required
def logout():
    user = current_user
    user.last_login_at, user.current_login_at = user.current_login_at, None
    user.last_login_ip, user.current_login_ip = user.current_login_ip, None
    db.session.commit()
    logout_user()

    return redirect(url_for("base_blueprint.login"))


## Errors

# 捕捉全局状态码
@blueprint.app_errorhandler(403)
def access_forbidden(error):
    return render_template("errors/page_403.html"), 403


@blueprint.app_errorhandler(404)
def not_found_error(error):
    return render_template("errors/page_404.html"), 404


@blueprint.app_errorhandler(500)
def internal_error(error):
    return render_template("errors/page_500.html"), 500


# 捕捉当前蓝图下状态码
@blueprint.app_errorhandler(403)
def access_forbidden_local(error):
    return render_template("errors/page_403.html"), 403
