Plone RESTish API
=================

Reference: http://restcookbook.com/HTTP%20Methods/put-vs-post/

Create a document (in the portal root)::

  POST /plone/++api++1/json HTTP/1.1
  Host: http://nohost
  Content-Type: application/json
  {
    "title": "A document",
    "description": "Test",
    "body": "<p>Some <i>HTML</i></p>"
  }

  HTTP/1.1 201 Created
  Location: /plone/++api++1/json/a-document

Retrieve an existing document (at ``/plone/a-document``)::

  GET /plone/++api++1/json/a-document HTTP/1.1
  Host: http://nohost

  HTTP/1.1 200 OK
  Content-Type: application/json
  {
    "title": "A document",
    "description": "Test",
    "body": "<p>Some <i>HTML</i></p>"
  }

Modify an existing document (at ``/plone/a-document``)::

  PUT /plone/++api++1/json/a-document HTTP/1.1
  Host: http://nohost
  Content-Type: application/json
  {
    "body": "<p>Some <em>semantic HTML</em></p>"
  }

  HTTP/1.1 200 OK
  Content-Type: application/json
  {
    "title": "A document",
    "description": "Test",
    "body": "<p>Some <em>semantic HTML</em></p>"
  }

Delete an existing document (at ``/plone/a-document``)::

  DELETE /plone/++api++1/json/a-document HTTP/1.1
  Host: http://nohost

  HTTP/1.1 410 Gone
  Location: /plone/++api++1/json/@@listing
