# -*- coding: utf-8 -*-
from plone.app.angularjs.testing import\
    PLONE_APP_ANGULARJS_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser

import unittest2 as unittest


class TestAngularAppPortalRootTraverser(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_portal_root_returns_angular_app(self):
        self.browser.open(self.portal_url)
        self.assertTrue('ng-app="ploneApp"' in self.browser.contents)

    def test_portal_root_folder_listing_returns_angular_app(self):
        self.browser.open(self.portal_url + '/folder_listing')
        self.assertTrue('ng-app="ploneApp"' in self.browser.contents)

    def test_portal_root_folder_contents_returns_angular_app(self):
        self.browser.open(self.portal_url + '/folder_contents')
        self.assertTrue('ng-app="ploneApp"' in self.browser.contents)

    def test_portal_root_returns_angular_app_if_frontpage_exists(self):
        self.portal.invokeFactory(
            'Document', id='front-page', title='Front Page'
        )
        self.browser.open(self.portal_url)
        self.assertTrue('ng-app="ploneApp"' in self.browser.contents)


class TestAngularAppRedirectorTraverser(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_document_redirects_to_angular_app(self):
        self.portal.invokeFactory(
            'Document', id='doc1', title='Document 1'
        )
        # XXX: Why the hell do we need this here? Using a functional
        # test fixture should be enough.
        import transaction
        transaction.commit()
        self.browser.open(self.portal_url + '/doc1')
        self.assertTrue('ng-app="ploneApp"' in self.browser.contents)
