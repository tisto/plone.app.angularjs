.. contents::

plone.app.angularjs
===================

Create a simple angular app within Plone
----------------------------------------

Create app dir::

  cd src/plone/app/angularjs
  mkdir app
  touch app/__init__.py

configure.zcml::

  <include package=".app" />

app/configure.zcml::

  <configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:zcml="http://namespaces.zope.org/zcml"
    i18n_domain="plone.app.angularjs">

    <browser:page
      name="index.html"
      for="*"
      template="index.html"
      permission="zope2.View"
      />

  </configure>

app/index.html::

  <!doctype html>
  <html ng-app>
  <head>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.3.0-beta.5/angular.min.js"></script>
  </head>
  <body>
    <div>
      <label>Name:</label>
      <input type="text" ng-model="yourName" placeholder="Enter a name here">
      <hr>
      <h1>Hello {{yourName}}!</h1>
    </div>
  </body>
  </html>
