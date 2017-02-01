#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""users/forms.py: User forms."""

from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):
    matricula = StringField(u'Matrícula', validators=[Length(min=3, max=10), DataRequired()])
    #email = StringField('Correo', validators=[Length(min=6, max=120)])
    #notify = BooleanField('Notificar por Twitter', default=True)
