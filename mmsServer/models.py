#!/usr/bin/env python

# models.py
# SQLAlchemy models for the TinkerMill Member Management System (MMS).

### IMPORTS ###
from mmsServer import db
from sqlalchemy.dialects import mysql

### GLOBALS ###

### CLASSES ###
class Member( db.Model):
    __tablename__ = 'members'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    membership_id = db.Column( db.Integer) # This is a manually managed foreign key into "Membership"
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
        # Debug representation
        return '<Member: %r %r>' % ( self.first_name, self.last_name)
    
    def __str__( self):
        # Debug representation
        return '<Member: %r %r>' % ( self.first_name, self.last_name)

class Membership( db.Model):
    __tablename__ = 'memberships'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    membershiptype_id = db.Column( db.Integer, db.ForeignKey( 'membershiptypes.id'))
    billing_address_line1 = db.Column( db.Text)
    billing_address_line2 = db.Column( db.Text)
    billing_address_state = db.Column( db.String( 2))
    billing_address_zipcode = db.Column( db.String( 10))
    primary_member_id = db.Column( db.Integer, db.ForeignKey( 'members.id'), nullable = False)
    start_date = db.Column( db.Date, nullable = False)
    
    def __repr__( self):
        # Debug representation
        return '<Membership: %r>' % ( self.id, )
    
    def __str__( self):
        # Debug representation
        return '<Membership: %r>' % ( self.id, )

class Membershiptype( db.Model):
    __tablename__ = 'membershiptypes'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    name = db.Column( db.String( 255), unique = True, nullable = False)
    memberships = db.relationship( 'Membership', backref = 'type', lazy = 'dynamic') # This is sweet SQLAlchemy magic
    
    def __repr__( self):
        # Debug representation
        return '<Membershiptype: %r>' % ( self.id, )
    
    def __str__( self):
        # Debug representation
        return '<Membershiptype: %r>' % ( self.id, )

class Memberpic( db.Model):
    __tablename__ = 'memberpics'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    member_id = db.Column( db.Integer, db.ForeignKey( 'members.id'), nullable = False)
    image_type = db.Column( db.String( 3), nullable = False)
    image_blob = db.Column( mysql.LONGBLOB, nullable = False)
    
    def __repr__( self):
        # Debug representation
        return '<Image for Memebr: %r>' % ( self.member_id, )
    
    def __str__( self):
        # Debug representation
        return '<Image for Memebr: %r>' % ( self.member_id, )

class Capability( db.Model):
    __tablename__ = 'capabilities'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    capabilitytype_id = db.Column( db.Integer, db.ForeignKey( 'capabilitytypes.id'))
    member_id = db.Column( db.Integer, db.ForeignKey( 'members.id'), nullable = False)
    start_date = db.Column( db.Date, nullable = False)
    
    def __repr__( self):
        # Debug representation
        return '<Capability: %r>' % ( self.id, )
    
    def __str__( self):
        # Debug representation
        return '<Capability: %r>' % ( self.id, )

class Capabilitytype( db.Model):
    __tablename__ = 'capabilitytypes'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    name = db.Column( db.String( 255), unique = True, nullable = False)
    capabilities = db.relationship( 'Capability', backref = 'type', lazy = 'dynamic') # This is sweet SQLAlchemy magic
    
    def __repr__( self):
        # Debug representation
        return '<Capabilitytype: %r>' % ( self.id, )
    
    def __str__( self):
        # Debug representation
        return '<Capabilitytype: %r>' % ( self.id, )

class Accessdevice( db.Model):
    __tablename__ = 'accessdevices'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    location = db.Column( db.String( 255), nullable = False)
    capabilitytype_id = db.Column( db.Integer, db.ForeignKey( 'capabilitytypes.id')) # This type enables access
    api_key = db.Column( db.String( 255), unique = True, nullable = False) # Might convert this to a key pair.
    ## NOTE: An 'Accessdevice' should be inserted for each RFID endpoint.  The RPi should be configured with multiple
    ##       api-keys when acting as the gateway for multiple RFID endpoints.
    
    def __repr__( self):
        # Debug representation
        return '<Accessdevice: %r>' % ( self.id, )
    
    def __str__( self):
        # Debug representation
        return '<Accessdevice: %r>' % ( self.id, )

class Logaccessdevice( db.Model):
    __tablename__ = 'logaccessdevices'
    
    # Columns
    id = db.Column( db.Integer, primary_key = True)
    device_id = db.Column( db.Integer, db.ForeignKey( 'accessdevices.id'), nullable = False)
    member_id = db.Column( db.Integer, db.ForeignKey( 'members.id'), nullable = False)
    timestamp = db.Column( db.DateTime, nullable = False) # Might convert this to a key pair
    
    def __repr__( self):
        # Debug representation
        return '<Accessdevice: %r>' % ( self.id, )
    
    def __str__( self):
        # Debug representation
        return '<Accessdevice: %r>' % ( self.id, )

### FUNCTIONS ###

