# -*- coding: utf-8 -*-
"""
oathldap_web.forms - forms declarations
"""

from wtforms import (
    Form,
    StringField,
    PasswordField,
    SubmitField,
    validators,
)


class TokenResetForm(Form):
    """
    token reset form
    """
    admin = StringField(
        'Admin username',
        [
            validators.Length(min=4, max=25),
            validators.InputRequired(),
            validators.Regexp('^[a-zA-Z_.-]+$'),
        ],
    )
    password = PasswordField(
        'New Password',
        [
            validators.InputRequired(),
        ],
    )
    serial = StringField(
        'Device serial',
        [
            validators.Length(min=4, max=32),
            validators.InputRequired(),
            validators.Regexp('^[0-9]*$'),
        ],
    )
    confirm = StringField(
        'Confirmation hash',
        [
            validators.Optional(strip_whitespace=True),
            validators.Regexp('^[0-9a-fA-F]*$'),
        ],
    )
    submit = SubmitField()
