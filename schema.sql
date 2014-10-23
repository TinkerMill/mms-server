drop table if exists member;
drop table if exists membership;
drop table if exists devices;
drop table if exists entitlements;
drop table if exists usageLog;

create table member (
  id integer primary key autoincrement,
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

insert into member ('id','membership_id', 'firstName','lastName','companyName','email',
'phone','emergencyPhone','emergencyName','emergencyEmail','accountDisabled',
'isMinor', 'startDate', 'roleId','passwordHash', 'badgeSerialNumber') VALUES
(0,0,'root','admin', 'tinkermill','admin@tinkermill.org','000-000-0000',
'noPhone','noName','noEmail',0, 0, CURRENT_TIMESTAMP, 0, '', 'a2f49dk3' );


create table membership (
  id integer primary key autoincrement,
  membershipType integer,
  numMembers integer,
  billingAddressLine1 text,
  billingAddressLine2 text,
  billingAddressState text,
  billingAddressZipcode text,
  primaryMemberId integer,
  startDate integer
);

create table devices (
  id integer primary key autoincrement,
  deviceName text not null,
  certificiateRequired integer
);

create table entitlements (
  id integer primary key autoincrement,
  deviceId integer,
  memberId integer,
  grantedDate integer,
  active boolean
);

insert into entitlements ('deviceId','memberId','grantedDate', 'active') values (0,0,CURRENT_TIMESTAMP,1);

create table usageLog (
  id integer primary key autoincrement,
  timeStamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  memberId integer,
  deviceId integer,
  message text
);