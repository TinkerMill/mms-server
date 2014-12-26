#!/usr/bin/env python

# __init__.py

### IMPORTS ###
import os

import sys
import os.path
import time
import json
from datetime import datetime

from flask import Flask, g, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


### GLOBALS ###
# Have to setup the template directory when this is a package
#   http://stackoverflow.com/questions/8478404/flask-doesnt-locate-template-directory-when-running-with-twisted
templateDirectory = os.path.join( os.path.dirname( os.path.abspath(__file__)), 'templates')

app = Flask( 'mmsServer', template_folder = templateDirectory)

#app.config.update(dict(DATABASE="tinkermill.db"))
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join( os.path.dirname( __file__), 'mms.db')
SQLALCHEMY_DATABASE_URI = 'mysql://root:strangehat@localhost/mms_server'

app.config[ 'SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy( app)

### VIEWS ###

# This should be used in the modules to import the models for use
from mmsServer.models import Member
from mmsServer.models import Logaccessdevice
from mmsServer.models import Accessdevice

# create everything
db.create_all()
db.session.commit()

### FUNCTIONS ###

### ROUTING ###
def log(deviceId, memberId, logMessage):
    """log access to the API. will add a timestamp to the logs

    Args:
       deviceId   (int):  The ID of the device
       memberId   (int):  The ID of the member
       message (string):  message describing what happened

    Returns:
       nothing

    """
    l = Logaccessdevice(device_id = deviceId, member_id = memberId, message=logMessage, timestamp=datetime.now() )
    db.session.add(l)
    db.session.commit()

@app.route("/checkAccess/<deviceId>/<serialNumber>")
def checkAccess(deviceId=None, serialNumber=None):
    """Return if serialNumber has access to current device

    Given a number off the RFID badge, lookup the user that is associated
    with that number, and then check if that user has access to that deviceid

    # test with :
    # http://localhost:5000/checkAccess/0/a2f49dk3   <- YAY
    # http://localhost:5000/checkAccess/0/a2f49dk33  <- FAIL
    Args:
       deviceId (int):  The ID of the device
       serialNumber (string) : the Serial number on the badge

    Returns:
       JSON  The return code::

          {status: true, message: "Success" } -- Success!
          {status: false, message: "fail reason" } -- No good.

    """

    log(deviceId, memberId, "Requesting Access for serial:" + serialNumber)

    m = Member.query.filter(User.serial == serialNumber).first()

    if m and m.account_disabled == False:
        log(deviceId, memberId, "Granted Access")
        return json.dumps({'status': True, 'message': "Success"})
    else:
        log(deviceId, memberId, "Denined Access : Access has been revoked")
        return json.dumps({'status': False, 'message': "Access has been revoked"})

@app.route("/log/usageLog")
def showLogusageLog():
    """
    Show the usage log, which shows what memberId's are trying
    to accomplish.

    http://localhost:5000/log/usageLog
    """
    logData = ""
    return render_template('usageLog.html', logData=logData)

@app.route("/list/members")
def listMembers():
    mlist=""
    return render_template('memberList.html', mlist=mlist)

@app.route("/processData" ,  methods=['POST'])
def processData():
    """take a cmd structure to update a table. see the testData.html
    in the static folder to see how to send valid data to this endpoint.

    This will be used to create new records and update existing records
    base on the cmd (update/new)

    Args:
       cmd  : is this new or an update
       table: the table to modify

    Returns:
       JSON  The return code::

          {status: true, message: "Success" } -- Success!
          {status: false, message: "fail reason" } -- No good.

    """

    dataStruct   = request.form
    cmd   = dataStruct['cmd']
    table = dataStruct['table']
    response = '{status: false, message: "no valid path" }'

    # if acl check does not return true then fail to make the update
    if not checkAcl(dataStruct['username'], dataStruct['passwordHash'] , cmd, table, get_db()):
        print cmd
        return '{status: false, message: "ACL Fail Check" }'

    # when creating functions to handle data, pass in the dataStruct, and get_db()
    # which will give it access to the database
    # see the response format above to see what kind of string/JSON to return to the client
    # so it knows what happened.
    if cmd == "new" and table == "member":
        response = newMember(dataStruct, get_db() )

    if cmd == "update" and table == "member":
        response = updateMember(dataStruct, get_db() )

    return response

@app.route("/")
def index():
    """main landing page

    """
    return render_template('index.html')


### MAIN ###
def main():
    app.run()

if __name__ == '__main__':
    main()
