# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.app.angularjs.testing import\
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING
from plone.app.angularjs.traversal import AngularAppPortalRootTraverser
from plone.app.angularjs.traversal import AngularAppRedirectorTraverser


class TestAngularAppPortalRootTraverser(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_portal_root_folder_listing_returns_angular_app(self):
        self.request.URL = 'http://nohost/plone/folder_listing'
        traversal = AngularAppPortalRootTraverser(self.portal, self.request)
        view = traversal.publishTraverse(self.request, "folder_listing")
        self.assertTrue('ng-app' in view)

    def test_front_page_returns_angular_app(self):
        self.request.URL = 'http://nohost/plone/front-page'
        traversal = AngularAppPortalRootTraverser(self.portal, self.request)
        view = traversal.publishTraverse(self.request, "front-page")
        self.assertTrue('ng-app' in view)


class TestAngularAppRedirectorTraverser(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_document_view_returns_angular_app(self):
        self.portal.invokeFactory('Document', 'doc1')
        self.request.URL = 'http://nohost/plone/doc1'
        traversal = AngularAppRedirectorTraverser(
            self.portal.doc1, self.request
        )
        view = traversal.publishTraverse(self.request, "view")
        self.assertTrue('ng-app' in view)

    def test_document_edit_returns_angular_app(self):
        self.portal.invokeFactory('Document', 'doc1')
        self.request.URL = 'http://nohost/plone/doc1'
        traversal = AngularAppRedirectorTraverser(
            self.portal.doc1, self.request
        )
        view = traversal.publishTraverse(self.request, "edit")
        self.assertTrue('ng-app' in view)

    def test_folder_view_returns_angular_app(self):
        self.portal.invokeFactory('Folder', 'folder1')
        self.request.URL = 'http://nohost/plone/folder1'
        traversal = AngularAppRedirectorTraverser(
            self.portal.folder1, self.request
        )
        view = traversal.publishTraverse(self.request, "view")
        self.assertTrue('ng-app' in view)

    def test_folder_contents_returns_angular_app(self):
        self.portal.invokeFactory('Folder', 'folder1')
        self.request.URL = 'http://nohost/plone/folder1'
        traversal = AngularAppRedirectorTraverser(
            self.portal.folder1, self.request
        )
        view = traversal.publishTraverse(self.request, "folder_contents")
        self.assertTrue('ng-app' in view)
