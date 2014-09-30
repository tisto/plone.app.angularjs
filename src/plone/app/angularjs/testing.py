# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig
import plone.app.angularjs
import plone.app.caching


class PloneAppAngularJsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            plone.app.angularjs,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.angularjs:default')


class PloneAppCachingLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            plone.app.caching,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        # Enable Caching
        applyProfile(portal, 'plone.app.caching:default')
        applyProfile(portal, 'plone.app.caching:without-caching-proxy')
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        registry['plone.caching.interfaces.ICacheSettings.enabled'] = True


PLONE_APP_ANGULARJS_FIXTURE = PloneAppAngularJsLayer()
PLONE_APP_CACHING_FIXTURE = PloneAppCachingLayer()

PLONE_APP_ANGULARJS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_ANGULARJS_FIXTURE,),
    name="PloneAppAngularJs:Integration"
)

PLONE_APP_ANGULARJS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_ANGULARJS_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PloneAppAngularJs:Functional"
)

PLONE_APP_ANGULARJS_WITH_CACHING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(
        PLONE_APP_ANGULARJS_FUNCTIONAL_TESTING,
        PLONE_APP_CACHING_FIXTURE,
    ),
    name="PloneAppAngularJs:Functional"
)

PLONE_APP_ANGULARJS_ROBOT_TESTING = FunctionalTesting(
    bases=(
        PLONE_APP_ANGULARJS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name="PloneAppAngularJs:Robot"
)
