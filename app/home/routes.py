#!/usr/bin/python
# -*- coding:utf-8 -*-

import operator
from functools import reduce

from flask import render_template, request
from flask_login import login_required, current_user
from sqlalchemy import and_

import app.utils as autils
from app.home import blueprint
from app.home.models import Announcement, Announcement_read
from configs.config import Config


@blueprint.route("/")
@blueprint.route("/index")
@login_required
def index():
    return render_template("index.html")


@blueprint.route("/<template>")
@login_required
def route_template(template):
    return render_template(template + ".html")


@blueprint.route("/message/<id>", methods=["GET"])
@login_required
def message(id):
    pass


@blueprint.route("/message/read/<id>", methods=["GET"])
@login_required
def readmessage(id):
    pass


@blueprint.route("/message/readall", methods=["POST"])
@login_required
def readall():
    pass


@blueprint.route("/pushmsg", methods=["POST"])
@login_required
def pushmsg():
    announcement = Announcement()


@blueprint.route("/messages", methods=["GET"])
@login_required
def messages():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("page_size", Config.PAGE_SIZE))
    message_status = request.args.get("status", 0)  # 未读消息为0
    message_type = request.args.get("type", "ALL")  # 默认所有消息
    show = int(request.args.get("show", 0))  # 默认查询消息

    if message_status:
        if message_type == "ALL":
            paginate = (
                Announcement.query.join(
                    Announcement_read,
                    Announcement.id == Announcement_read.announcement_id,
                )
                    .filter(Announcement_read.user_id == current_user.id)
                    .order_by(Announcement.id.desc())
                    .paginate(page, per_page, error_out=True)
            )
        else:
            paginate = (
                Announcement.query.join(
                    Announcement_read,
                    Announcement.id == Announcement_read.announcement_id,
                )
                    .filter(
                    and_(
                        Announcement_read.user_id == current_user.id,
                        Announcement.type == message_type,
                    )
                )
                    .order_by(Announcement.id.desc())
                    .paginate(page, per_page, error_out=True)
            )
    else:
        read_id = (
            Announcement_read.query.with_entities(Announcement_read.announcement_id)
                .filter(Announcement_read.user_id == current_user.id)
                .all()
        )

        if len(read_id) >= 1:
            read_id = reduce(operator.add, read_id)
        else:
            read_id = tuple(0)

        if message_type == "ALL":
            paginate = (
                Announcement.query.filter(Announcement.id.notin_(read_id))
                    .order_by(Announcement.id.desc())
                    .paginate(page, per_page, error_out=True)
            )
        else:
            paginate = (
                Announcement.query.filter(
                    and_(
                        Announcement.id.notin_(read_id),
                        Announcement.type == message_type,
                    )
                )
                    .order_by(Announcement.id.desc())
                    .paginate(page, per_page, error_out=True)
            )

    records = paginate.items
    total_pages = paginate.pages
    total = paginate.total

    if show:
        return render_template(
            "message.html",
            name=current_user.username,
            users=records,
            pagination=paginate,
        )
    else:
        return (
            {
                "total": total,
                "page": page,
                "per_page": per_page,
                "messages": autils.paginate2json(records),
            },
            200,
        )
