#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from notificamesta import create_app

app = create_app('development')

if __name__ == "__main__":
    app.run()
