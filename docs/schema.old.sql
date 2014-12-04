-- NOTE: The tables are being handled by SQLAlchemy.  Use SQLAlchemy to create the tables!

-- Drop all of the tables to wipe the database
drop table if exists member;
drop table if exists membership;
drop table if exists devices;
drop table if exists entitlements;
drop table if exists usageLog;

-- Create a members table
create table member (
  id integer primary key auto_increment,
  membership_id integer,
  firstName text not null,
  lastName text not null,
  companyName text not null,
  email text not null,
  phone text not null,
  emergencyPhone text not null,
  emergencyName text not null,
  emergencyEmail text not null,
  accountDisabled boolean,
  isMinor boolean,
  gaurdianName text,
  startDate integer,
  roleId integer,
  passwordHash text not null,
  badgeSerialNumber text
);

-- Create a membership status table
create table membership (
  id integer primary key auto_increment,
  membershipType integer,
  numMembers integer,
  billingAddressLine1 text,
  billingAddressLine2 text,
  billingAddressState text,
  billingAddressZipcode text,
  primaryMemberId integer,
  startDate integer
);

-- Create a table to store the access devices
create table devices (
  id integer primary key auto_increment,
  deviceName text not null,
  certificiateRequired integer
);

-- Create a table to store member entitlements ( what members are allowed to access).
create table entitlements (
  id integer primary key auto_increment,
  deviceId integer,
  memberId integer,
  grantedDate integer,
  active boolean
);

-- Create an access log
-- NOTE: MariaDB 5.5 doesn't allow CURRENT_TIMESTAMP to be a default value.  The following was used instead:
--   timeStamp DATETIME
create table usageLog (
  id integer primary key auto_increment,
  timeStamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  memberId integer,
  deviceId integer,
  message text
);

-- Insert an admin member into the members table
insert into member (
  id,
  membership_id,
  firstName,
  lastName,
  companyName,
  email,
  phone,
  emergencyPhone,
  emergencyName,
  emergencyEmail,
  accountDisabled,
  isMinor,
  startDate,
  roleId,
  passwordHash,
  badgeSerialNumber
) VALUES (
  0,
  0,
  'root',
  'admin',
  'tinkermill',
  'admin@tinkermill.org',
  '000-000-0000',
  'noPhone',
  'noName',
  'noEmail',
  0,
  0,
  CURRENT_TIMESTAMP,
  0,
  '',
  'a2f49dk3'
);

-- Insert an entitlement for the admin member
insert into entitlements (
  deviceId,
  memberId,
  grantedDate,
  active
) values (
  0,
  0,
  CURRENT_TIMESTAMP,
  1
);
