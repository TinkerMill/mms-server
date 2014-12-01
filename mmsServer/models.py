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
    first_name = db.Column( db.Text, nullable = False)
    last_name = db.Column( db.Text)
    company_name = db.Column( db.Text)
    email = db.Column( db.String( 255), unique = True, index = True, nullable = False)
    phone = db.Column( db.Text)
    emergency_phone = db.Column( db.Text)
    emergency_name = db.Column( db.Text)
    emergency_email = db.Column( db.Text)
    account_disabled = db.Column( db.Boolean, nullable = False)
    is_minor = db.Column( db.Boolean, nullable = False)
    guardian_name = db.Column( db.Text)
    start_date = db.Column( db.Date, nullable = False)
    role_id = db.Column( db.Integer, nullable = False)
    password_hash = db.Column( db.Text)
    badge_serial = db.Column( db.String( 16), unique = True)
    
    def __repr__( self):
        # Debug representatino
        return '<User: %r %r>' % ( self.firstName, self.lastName)
    
    def __str__( self):
        # Debug representatino
        return '<User: %r %r>' % ( self.firstName, self.lastName)

### FUNCTIONS ###

