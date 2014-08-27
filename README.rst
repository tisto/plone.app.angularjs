plone.app.angularjs
===================

Experimental AngularJS-based front end for the Plone CMS.

Contents
--------

.. contents::

Prerequisits
------------

Install Bower::

  $ sudo npm install -g bower

Install Grunt::

  $ sudo npm install -g grunt-cli

Buildout
--------

Run buildout::

  $ python bootstrap.py
  $ bin/buildout

Buildout will run "bower install" to install all js dependencies defined in bower.json.
