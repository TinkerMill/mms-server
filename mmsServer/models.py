#!/usr/bin/env python

# models.py
# SQLAlchemy models for the TinkerMill Member Management System (MMS).

### IMPORTS ###
from mmsServer import db

### GLOBALS ###

### CLASSES ###
class Member( db.Model):
    __tablename__ = 'members'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    membership_id = db.Column( db.Integer) # This becomes a foreign key into "Membership"
    firstName = db.Column( db.Text, nullable = False)
    lastName = db.Column( db.Text)
    companyName = db.Column( db.Text)
    email = db.Column( db.Text, unique = True, index = True, nullable = False)
    phone = db.Column( db.Text)
    emergencyPhone = db.Column( db.Text)
    emergencyName = db.Column( db.Text)
    emergencyEmail = db.Column( db.Text)
    accountDisabled = db.Column( db.Boolean, nullable = False)
    isMinor = db.Column( db.Boolean, nullable = False)
    gaurdianName = db.Column( db.Text)
    startDate = db.Column( db.Date, nullable = False)
    roleId = db.Column( db.Integer, nullable = False)
    passwordHash = db.Column( db.Text)
    badgeSerialNumber = db.Column( db.String( 16), unique = True)
    
    def __repr__( self):
        # Debug representatino
        return '<User: %r %r>' % ( self.firstName, self.lastName)
    
    def __str__( self):
        # Debug representatino
        return '<User: %r %r>' % ( self.firstName, self.lastName)

### FUNCTIONS ###

