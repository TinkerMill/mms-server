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
    account_disabled = db.Column( db.Boolean, nullable = False, default = False)
    is_minor = db.Column( db.Boolean, nullable = False, default = False)
    guardian_name = db.Column( db.Text)
    start_date = db.Column( db.Date, nullable = False)
    role_id = db.Column( db.Integer, nullable = False, default = 1) # role_ids: 3 -> admin, 1 -> member
    password_hash = db.Column( db.Text)
    
    def __repr__( self):
        # Debug representatino
        return '<Member: %r %r>' % ( self.first_name, self.last_name)
    
    def __str__( self):
        # Debug representatino
        return '<Member: %r %r>' % ( self.first_name, self.last_name)

class Membership( db.Model):
    __tablename__ = 'memberships'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    membershiptype_id = db.Column( db.Integer) # This becomes a foreign key into "MembershipType"
    billing_address_line1 = db.Column( db.Text)
    billing_address_line2 = db.Column( db.Text)
    billing_address_state = db.Column( db.String( 2))
    billing_address_zipcode = db.Column( db.String( 10))
    primary_member_id = db.Column( db.Integer, db.ForeignKey( 'member.id'), nullable = False) # This becomes a foreign key into "Member"
    start_date = db.Column( db.Date, nullable = False)
    
    def __repr__( self):
        # Debug representatino
        return '<Membership: %r>' % ( self.id, )
    
    def __str__( self):
        # Debug representatino
        return '<Membership: %r>' % ( self.id, )

### FUNCTIONS ###

