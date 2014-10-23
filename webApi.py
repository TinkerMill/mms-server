import sys
import ConfigParser
import os.path
import time
import sqlite3
import json

from flask import Flask, g, render_template

config = ConfigParser.SafeConfigParser()

# configure the app
app = Flask("tinkermillWebApi")
app.config.update(dict(DATABASE="tinkermill.db"))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')
    
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

@app.route("/checkAccess/<deviceId>/<memberId>")
def checkAccess(deviceId=None, memberId=None):
    """Return if user has access to current device

    Args:
       deviceId (int):  The ID of the device
       memberId (int):  The ID of the member
    
    Returns:
       JSON  The return code::

          {status: true, message: "Success" } -- Success!
          {status: false, message: "fail reason" } -- No good.
          
    """
    log(deviceId, memberId, "Requesting Access")
    
    db = get_db()
    for status in query_db("select active from entitlements where memberId=%s and deviceId=%s" % (memberId, deviceId)):
        if status[0] == 1:
            log(deviceId, memberId, "Granted Access")
            return json.dumps({'status': True, 'message': "Success"})
        if status[0] == 0:
            log(deviceId, memberId, "Denined Access : Access has been revoked")
            return json.dumps({'status': False, 'message': "Access has been revoked"})
    
    log(deviceId, memberId, "Denined Access : No Access found")       
    return json.dumps({'status': True, 'message': "No Access found."})

@app.route("/")
def index():
    """main landing page

    """
    return render_template('index.html')



if __name__ == '__main__':
    
    # read configuration file
    if os.path.isfile("run.cfg"):
        config.read('run.cfg')
        # config.get[Float/Int/Boolean]('config1', 'varname')
 
    app.run()

