from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import plone.app.angularjs


PLONE_APP_ANGULARJS = PloneWithPackageLayer(
    zcml_package=plone.app.angularjs,
    zcml_filename='testing.zcml',
    gs_profile_id='plone.app.angularjs:testing',
    name="PLONE_APP_ANGULARJS")

PLONE_APP_ANGULARJS_INTEGRATION = IntegrationTesting(
    bases=(PLONE_APP_ANGULARJS, ),
    name="PLONE_APP_ANGULARJS_INTEGRATION")

PLONE_APP_ANGULARJS_FUNCTIONAL = FunctionalTesting(
    bases=(PLONE_APP_ANGULARJS, ),
    name="PLONE_APP_ANGULARJS_FUNCTIONAL")
