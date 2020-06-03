#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import render_template

from app.tools import blueprint


@blueprint.route("/")
@blueprint.route("/all", methods=["GET"])
def route_default():
    return render_template("tools.html")


@blueprint.route("/config", methods=["POST"])
def config():
    pass


@blueprint.route("/download")
def download():
    pass
