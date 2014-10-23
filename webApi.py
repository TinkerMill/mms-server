import sys
import os.path
import time
import sqlite3
import json

from flask import Flask, g, render_template

# import all the local functions
from createSerialNumber import createSerialNumber
from acl import checkAcl

# configure the app
app = Flask("tinkermillWebApi")
app.config.update(dict(DATABASE="tinkermill.db"))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

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
    
def insert(table, fields=(), values=()):
    # g.db is the database connection
    cur = g.sqlite_db.cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    g.sqlite_db.commit()
    id = cur.lastrowid
    cur.close()
    return id

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
      
    db.commit()
    
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
    
@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

@app.route("/checkAccess/<deviceId>/<memberId>/<serialNumber>")
def checkAccess(deviceId=None, memberId=None, serialNumber=None):
    """Return if user has access to current device

    Args:
       deviceId (int):  The ID of the device
       memberId (int):  The ID of the member
       serialNumber (string) : the Serial number on the badge
       
    Returns:
       JSON  The return code::

          {status: true, message: "Success" } -- Success!
          {status: false, message: "fail reason" } -- No good.
          
    """
    log(deviceId, memberId, "Requesting Access")
    
    db = get_db()
    sql = "select entitlements.active from entitlements,member where member.id=entitlements.memberId and entitlements.memberId=%s and entitlements.deviceId=%s and member.badgeSerialNumber='%s'" % (memberId, deviceId, serialNumber)
    print sql
    for status in query_db(sql):
        if status[0] == 1:
            log(deviceId, memberId, "Granted Access")
            return json.dumps({'status': True, 'message': "Success"})
        if status[0] == 0:
            log(deviceId, memberId, "Denined Access : Access has been revoked")
            return json.dumps({'status': False, 'message': "Access has been revoked"})
    
    log(deviceId, memberId, "Denined Access : No Access found")       
    return json.dumps({'status': False, 'message': "No Access found."})

@app.route("/list/members")
def listMembers():
    mlist = query_db("select * from member")
    return render_template('memberList.html', mlist=mlist)
    
@app.route("/create/member/" , methods=['POST'])
def createMember():
    pass

@app.route("/update/member/" ,  methods=['POST'])
def updateMember():
    """take a cmd structure to update a member

    Args:
       cmd : a JSON request that contains the actions to perform on the user
       
    Returns:
       JSON  The return code::

          {status: true, message: "Success" } -- Success!
          {status: false, message: "fail reason" } -- No good.
          
    """
    # load the cmd structure into a python objec to work with
    cmd=json.loads(request.form['cmd'])
    
    # if acl check does not return true then fail to make the update
    if not checkAcl(cmd):
        print cmd
        return '{status: false, message: "ACL Fail Check" }'
    
    
    return '{status: false, message: "fail reason" }'

@app.route("/")
def index():
    """main landing page

    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

