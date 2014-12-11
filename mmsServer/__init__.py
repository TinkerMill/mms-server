#!/usr/bin/env python

# __init__.py

### IMPORTS ###
import os

import sys
import os.path
import time
import sqlite3
import json

from flask import Flask, g, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

from createSerialNumber import createSerialNumber
from acl import checkAcl
from newMember import newMember
from updateMember import updateMember

### GLOBALS ###
# Have to setup the template directory when this is a package
#   http://stackoverflow.com/questions/8478404/flask-doesnt-locate-template-directory-when-running-with-twisted
templateDirectory = os.path.join( os.path.dirname( os.path.abspath(__file__)), 'templates')

app = Flask( 'mmsServer', template_folder = templateDirectory)

#app.config.update(dict(DATABASE="tinkermill.db"))
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join( os.path.dirname( __file__), 'mms.db')
#SQLALCHEMY_DATABASE_URI = 'mysql://localhost/mms_server'

app.config[ 'SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy( app)

# This should be used in the modules to import the models for use
#from mmsServer import models

### VIEWS ###
# Import the needed views
from mmsServer.checkAccess import CheckAccess

# Setup the views
view_checkAccess = CheckAccess.as_view( 'checkAccess')

### FUNCTIONS ###
def log(deviceId, memberId, message):
    """log access to the API. will add a timestamp to the logs
    
    Args:
       deviceId   (int):  The ID of the device
       memberId   (int):  The ID of the member
       message (string):  message describing what happened
       
    Returns:
       nothing
          
    """
    cur = get_db().cursor()
    cur.execute("insert into usageLog ('deviceId','memberId','message') values (%s,%s,'%s')" %(deviceId, memberId, message))
    g.sqlite_db.commit()
    cur.close()

## HANDLED BY SQLAlchemy
#def insert(table, fields=(), values=()):
#    # g.db is the database connection
#    cur = g.sqlite_db.cursor()
#    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
#        table,
#        ', '.join(fields),
#        ', '.join(['?'] * len(values))
#    )
#    cur.execute(query, values)
#    g.sqlite_db.commit()
#    id = cur.lastrowid
#    cur.close()
#    return id

## HANDLED BY SQLAlchemy
#def connect_db():
#    """Connects to the specific database."""
#    rv = sqlite3.connect(app.config['DATABASE'])
#    rv.row_factory = sqlite3.Row
#    return rv

## HANDLED BY SQLAlchemy
#def init_db():
#    """Initializes the database."""
#    db = get_db()
#    with app.open_resource('schema.sql', mode='r') as f:
#        db.cursor().executescript(f.read())
#      
#    db.commit()

## HANDLED BY SQLAlchemy
#def get_db():
#    """Opens a new database connection if there is none yet for the
#    current application context.
#    """
#    if not hasattr(g, 'sqlite_db'):
#        g.sqlite_db = connect_db()
#    return g.sqlite_db

## HANDLED BY SQLAlchemy
#def query_db(query, args=(), one=False):
#    cur = get_db().execute(query, args)
#    rv = cur.fetchall()
#    cur.close()
#    return (rv[0] if rv else None) if one else rv
 
def getMemberIdFromSerial(serialNumber):
    db = get_db()
    sql = "select id from member where badgeSerialNumber='%s'" % (serialNumber)
    for id in query_db(sql):
        return str( id[0])
    return "-1"

#@app.cli.command('initdb')
#def initdb_command():
#    """Creates the database tables."""
#    init_db()
#    print('Initialized the database.')

### ROUTING ###
# NOTE: See http://flask.pocoo.org/docs/0.10/views/ for more information, specifically "Method Based Dispatching"
#       and "Method Views for APIs".

# /checkAccess
#   - Expects an mms-api-key header to be present and contain a UUID for the device.
#   - Expects an mms-badge header to be present and contain the serial number of an RFID badge.
app.add_url_rule( '/checkAccess', view_func = view_checkAccess, methods = [ 'GET', ])

# Other routing
@app.route("/matt")
def matt():
    return getMemberIdFromSerial('a2f49dk3')

@app.route("/log/usageLog")
def showLogusageLog():
    """
    Show the usage log, which shows what memberId's are trying
    to accomplish.
    
    http://localhost:5000/log/usageLog
    """
    logData = query_db("select * from usageLog")
    return render_template('usageLog.html', logData=logData)

@app.route("/list/members")
def listMembers():
    mlist = query_db("select * from member")
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

