#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""multas/views.py: Multas views."""

import click
from notificamesta import db
from flask import Blueprint, session, flash, redirect, url_for, render_template
#from .models import User


multas_blueprint = Blueprint(
    'multas', __name__,
    template_folder='templates'
)

