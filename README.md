mms-server
==========

The API server for the member management system.

User Stories
------------

User stories for the Member Maangment System are being kept on www.storiesonboard.com.  You can find them here: https://tinkermill.storiesonboard.com/#/m/tinkermill-management-system

If you need access, contact David Robinson at davidrobertrobinson@gmail.com

Vagrant Installation
--------------------
* checkout the source
* vagrant up
* vagrant ssh
* cd /vagrant
* run the server
* when you are finished (save) logout and run: vagrant destroy 

Installation
------------

1. Install a database engine.  We're using MariaDB ( a MySQL replacement) here at TinkerMill.
 * `apt-get install mariadb-server python-mysqldb`

1. Load the schema into the database.

1. Install python flask and friends.
 * `apt-get install python-flask`
 * `apt-get install python-sqlalchemy`
 * `apt-get install python-flask-login`
 * `apt-get install python-flask-sqlalchemy`

