# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter


from plone.app.angularjs.testing import\
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING

import json


class TestAngularJsTopNavigation(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_view_is_registered(self):
        self.assertTrue(
            getMultiAdapter(
                (self.portal, self.request),
                name="angularjs-top-navigation"
            )
        )

    def test_empty_navigation(self):
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-top-navigation"
        )
        view = view.__of__(self.portal)
        self.assertEqual(json.loads(view()), [])

    def test_document_in_navigation(self):
        self.portal.invokeFactory('Document', 'doc1', title='Document 1')
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-top-navigation"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(
            json.loads(view()),
            [{
                u'id': u'doc1',
                u'title': u'Document 1',
                u'description': u'',
                u'url': '#/doc1',
            }]
        )

    def test_do_not_show_excluded_from_nav_documents(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.exclude_from_nav = True
        self.portal.folder1.reindexObject(idxs=['exclude_from_nav'])
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-top-navigation"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(len(json.loads(view())), 0)


class TestAngularJsPortletNavigation(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_view_is_registered(self):
        self.assertTrue(
            getMultiAdapter(
                (self.portal, self.request),
                name="angularjs-portlet-navigation"
            )
        )

    def test_empty_navigation(self):
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-portlet-navigation"
        )
        view = view.__of__(self.portal)
        self.assertEqual(json.loads(view()), [])

    def test_document_in_navigation(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-portlet-navigation"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(
            json.loads(view()),
            [{
                u'id': u'folder1',
                u'title': u'Folder 1',
                u'description': u'',
                u'url': '#/folder1',
                u'children': []
            }]
        )

    def test_nested_document_in_navigation(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.invokeFactory(
            'Document', 'doc1', title='Document 1'
        )
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-portlet-navigation"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(
            json.loads(view())[0]['id'],
            'folder1'
        )
        self.assertEqual(
            json.loads(view())[0]['children'][0]['id'],
            'doc1'
        )

    def test_do_not_show_excluded_from_nav_documents(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.exclude_from_nav = True
        self.portal.folder1.reindexObject(idxs=['exclude_from_nav'])
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-portlet-navigation"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(len(json.loads(view())), 0)
