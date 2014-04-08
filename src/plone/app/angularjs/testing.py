from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig
import plone.app.angularjs


class PloneAppAngularJsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            plone.app.angularjs,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.angularjs:default')


PLONE_APP_ANGULARJS = PloneAppAngularJsLayer()

PLONE_APP_ANGULARJS_INTEGRATION = IntegrationTesting(
    bases=(PLONE_APP_ANGULARJS,),
    name="PloneAppAngularJs:Integration"
)

PLONE_APP_ANGULARJS_FUNCTIONAL = FunctionalTesting(
    bases=(PLONE_APP_ANGULARJS, z2.ZSERVER_FIXTURE),
    name="PloneAppAngularJs:Functional"
)
