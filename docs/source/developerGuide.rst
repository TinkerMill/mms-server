Developer Guide
===============

Installation
------------
here are the instructions for installing the api and getting it up and running

Python modules
^^^^^^^^^^^^^^
get the lastest pip::
 
  * pip install https://github.com/mitsuhiko/flask/tarball/master
  * pip install sqlite3
  
Database setup
^^^^^^^^^^^^^^

to create a new database or to clear out the current database::

  flask -a webApi.py init_db

Building the docs
^^^^^^^^^^^^^^^^^
To rebuild the documentation go into the docs directory and run the make.bat
or if you are unix you can run make and just build with the makefile in
that directory

Helpful links
^^^^^^^^^^^^^
* https://www.youtube.com/watch?feature=player_embedded&v=oJsUvBQyHBs
* http://sphinx-doc.org/man/sphinx-apidoc.html
* http://pylonsbook.com/en/1.0/documentation.html
* http://docutils.sourceforge.net/docs/user/rst/quickref.html


Notes to developers
===================

.. automodule:: webApi
   :members: checkAccess, processData


