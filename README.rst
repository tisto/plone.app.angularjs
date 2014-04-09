plone.app.angularjs
===================

Experimental AngularJS-based front end for the Plone CMS.

Contents
--------

.. contents::

Create a simple AngularJS App within Plone
------------------------------------------

Create app dir::

  cd src/plone/app/angularjs
  mkdir app
  touch app/__init__.py

configure.zcml::

  ...
  xmlns:plone="http://namespaces.plone.org/plone">

  <include package=".app" />
  <plone:static
    type="theme"
    directory="app"
    />

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

=> Go to app/index.html (without starting Zope)
=> Go to localhost:8080/Plone/index.html (after starting Zope)

setup.py::

  install_requires=[
      ...
      'plone.app.theming'
  ]

profiles/default/metadata.xml::

  <?xml version="1.0"?>
  <metadata>
    <version>0001</version>
    <dependencies>
      <dependency>profile-plone.app.theming:default</dependency>
    </dependencies>
  </metadata>

profiles/default/theme.xml::

  <theme>
    <name>plone.app.angularjs</name>
    <enabled>true</enabled>
  </theme>

index.html::

  <script src="++theme++plone.app.angularjs/scripts/app.js"></script>

app/rules.xml::

  <?xml version="1.0" encoding="UTF-8"?>
  <rules xmlns="http://namespaces.plone.org/diazo"
         xmlns:css="http://namespaces.plone.org/diazo/css"
         xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- CSS -->
    <replace content="/html/head/link[not(starts-with(@href, 'http'))]">
      <xsl:element name="link">
        <xsl:attribute name="rel">stylesheet</xsl:attribute>
        <xsl:attribute name="href">++theme++plone.app.angularjs/<xsl:value-of select="@href" /></xsl:attribute>
      </xsl:element>
    </replace>

    <!-- JAVASCRIPT -->
    <replace content="/html/head/script[not(starts-with(@src, 'http'))]">
      <xsl:element name="script">
        <xsl:attribute name="src">++theme++plone.app.angularjs/<xsl:value-of select="@src" /></xsl:attribute>
      </xsl:element>
    </replace>

    <!-- ANGULAR APP JAVASCRIPT -->
    <replace content="/html/body/script[starts-with(@src, 'scripts/')]">
      <xsl:element name="script">
        <xsl:attribute name="src">++theme++plone.app.angularjs/<xsl:value-of select="@src" /></xsl:attribute>
      </xsl:element>
    </replace>

  </rules>

app/manifest.cfg::

  [theme]
  title = plone.app.angularjs
  description =
  doctype = <!DOCTYPE html>
