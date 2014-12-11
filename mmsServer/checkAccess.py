#!/usr/bin/env python

# checkAccess.py
# checkAccess view and controller
# Used by 'Accessdevice' to check whether a given badge can access the resource controlled by the
#   identified ( by api-key currently) device.

### IMPORTS ###
import datetime
import uuid

from flask.views import MethodView

from mmsServer import models

### GLOBALS ###

### CLASSES ###
class CheckAccess( MethodView):
    # GET method for checking.
    #   - Expects an mms-api-key header to be present and contain a UUID for the device.
    #   - Expects an mms-badge header to be present and contain the serial number of an RFID badge.
    def get( self):
        # Get the headers.
        # Check the header validity (e.g. Is mms-api-key a valid UUID?)
        # Check if the badge has the capability required for the device ( Should this be a join?):
        #   - Get the device using the api-key.
        #   - Get the member using the badge.
        #   - Get the list of capabilities using the member.
        #   - If the list of capabilities contains a capability with a matching 'capabilitytype_id' to the device,
        #     log a successful access anf return a '200 OK'
        # Do we need to log failed attempts to the database, or is the log file good enough?
        # Return a '401 Unauthorized' ( should happen if the '200 OK' is not sent)
        pass

### FUNCTIONS ###

### MAIN ###
def main():
    pass

if __name__ == "__main__":
    main()

### MORE INFO ###
# Example moved from __init__.py
#@app.route("/checkAccess/<deviceId>/<serialNumber>")
#def checkAccess(deviceId=None, serialNumber=None):
#    """Return if serialNumber has access to current device
#    
#    Given a number off the RFID badge, lookup the user that is associated
#    with that number, and then check if that user has access to that deviceid
#    
#    # test with :
#    # http://localhost:5000/checkAccess/0/a2f49dk3   <- YAY 
#    # http://localhost:5000/checkAccess/0/a2f49dk33  <- FAIL
#    Args:
#       deviceId (int):  The ID of the device
#       serialNumber (string) : the Serial number on the badge
#       
#    Returns:
#       JSON  The return code::
#       
#          {status: true, message: "Success" } -- Success!
#          {status: false, message: "fail reason" } -- No good.
#    
#    """
#    
#    memberId = getMemberIdFromSerial(serialNumber)
#    log(deviceId, memberId, "Requesting Access for serial:" + serialNumber)
#    
#    db = get_db()
#    sql = "select entitlements.active from entitlements,member where member.id=entitlements.memberId and entitlements.memberId=%s and entitlements.deviceId=%s and member.badgeSerialNumber='%s'" % (memberId, deviceId, serialNumber)
#    print sql
#    for status in query_db(sql):
#        if status[0] == 1:
#            log(deviceId, memberId, "Granted Access")
#            return json.dumps({'status': True, 'message': "Success"})
#        if status[0] == 0:
#            log(deviceId, memberId, "Denined Access : Access has been revoked")
#            return json.dumps({'status': False, 'message': "Access has been revoked"})
#    
#    log(deviceId, memberId, "Denined Access : No Access found")       
#    return json.dumps({'status': False, 'message': "No Access found."})
