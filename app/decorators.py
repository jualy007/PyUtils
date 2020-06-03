#!/usr/bin/python
# -*- coding:utf-8 -*-

from functools import wraps

import jwt
from flask import request, jsonify
from flask_login import current_user

from configs.config import Config


def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if len(list(set(roles).intersection(set(current_user.roles())))) == 0:
                return jsonify("Permission Denied"), 403

            return func(*args, **kwargs)

        return wrapped

    return decorator


def auth_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if request.form.get("Auth") is not None:
            try:
                payload = jwt.decode(
                    request.form.get("Auth"),
                    Config.SECRET_KEY,
                    options={"verify_exp": True},
                )
                if payload:
                    return func(*args, **kwargs)
                else:
                    return jsonify("无效的Token"), 403

            except jwt.ExpiredSignatureError:
                return jsonify("Token过期"), 403
            except jwt.InvalidTokenError:
                return jsonify("无效的Token"), 403
        else:
            return jsonify("Need Authorized"), 403

    return wrapped
