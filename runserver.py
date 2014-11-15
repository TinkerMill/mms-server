#!/usr/bin/env python
# runserver.py
# This script runs the flask app in development mode.  DO NOT USE FOR PRODUCTION!

### IMPORTS ###
from mmsServer import app

### MAIN ###
app.run( host = "0.0.0.0", port = 5000, debug = True)

