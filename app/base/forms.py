#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo


## login and registration


class LoginForm(FlaskForm):
    username = StringField(
        label="User Name or User Email",
        id="username_login",
        validators=[DataRequired()],
    )
    password = PasswordField(
        label="User Password",
        id="pwd_login",
        validators=[InputRequired(), Length(8, 16)],
    )
    login = SubmitField(label="Login", id="login")


class CreateAccountForm(FlaskForm):
    username = StringField(
        "Username", id="username_create", validators=[DataRequired(), Length(6, 12)]
    )
    email = StringField(
        "Email", id="email_create", validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password", id="pwd_create", validators=[InputRequired(), Length(8, 16)]
    )
    repeatpassword = PasswordField(
        "RepeatPassword",
        id="repeatpwd_create",
        validators=[InputRequired(), Length(8, 16), EqualTo("password")],
    )
    register = SubmitField(label="Register", id="register")


class ForgetPasswdForm(FlaskForm):
    email = StringField(
        "Email", id="email_reset", validators=[InputRequired(), Email()]
    )
    confirm = SubmitField(label="Confirm", id="confirm")


class ResetPasswordForm(FlaskForm):
    email = StringField(
        "Email", id="email_reset", validators=[InputRequired(), Email()]
    )
    code = StringField("Code", id="", validators=[InputRequired(), Length(6)])
    password = PasswordField(
        "Password", id="pwd_reset", validators=[InputRequired(), Length(8, 16)]
    )
    repeatpassword = PasswordField(
        "RepeatPassword",
        id="repeatpwd_reset",
        validators=[InputRequired(), Length(8, 16), EqualTo("password")],
    )

    confirm = SubmitField(label="Confirm", id="reset")
