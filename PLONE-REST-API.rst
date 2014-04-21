How should a REST JSON API for Plone look like?
==============================================================================

Basics
======

Retrieve an existing document::

  http://nohost/plone/document/api/1.0/json [GET]

Create a new document:

  http://nohost/plone/document/api/1.0/json [POST] + DATA

Update an existing document (not supported by Zope Publisher)::

  http://nohost/plone/document/api/1.0/json [PUT] + DATA

Delete an existing document (not supported by Zope Publisher)::

  http://nohost/plone/document/api/1.0/json [DELETE]


Structure
=========

Retrieve a document within a folder::

  http://nohost/plone/folder/document/api/1.0/json [GET]


Further Reading
===============

http://www.vargascarlos.com/2013/02/pyramid-and-rest/
https://groups.google.com/forum/#!topic/pylons-discuss/_wK7GHB7J2k
http://glicksoftware.com/presentations/the-art-of-integrating-plone-with-webservices
http://de.slideshare.net/Jazkarta/plone-web-services-presentation
=> Plone lacks put/delete.
http://roy.gbiv.com/untangled/2008/no-rest-in-cmis
