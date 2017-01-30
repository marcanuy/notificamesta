#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from multaviso import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
