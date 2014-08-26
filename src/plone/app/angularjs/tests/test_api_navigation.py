# -*- coding: utf-8 -*-
from plone.app.angularjs.interfaces import IRestApi
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.angularjs.testing import\
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING
from zope.component import getUtility

import json
import unittest2 as unittest


class TestAngularJsTopNavigation(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.api = getUtility(IRestApi)

    def test_empty_navigation(self):
        self.assertEqual(json.loads(self.api.top_navigation(self.request)), [])

    def test_folder_in_navigation(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.reindexObject()

        self.assertTrue(self.api.top_navigation(self.request))
        self.assertEqual(
            json.loads(self.api.top_navigation(self.request)),
            [{
                u'id': u'folder1',
                u'title': u'Folder 1',
                u'description': u'',
                u'url': 'folder1',
            }]
        )

    def test_document_not_in_navigation(self):
        self.portal.invokeFactory('Document', 'doc1', title='Document 1')

        self.assertTrue(self.api.top_navigation(self.request))
        self.assertEqual(
            json.loads(self.api.top_navigation(self.request)),
            []
        )

    def test_do_not_show_excluded_from_nav_documents(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.exclude_from_nav = True
        self.portal.folder1.reindexObject(idxs=['exclude_from_nav'])

        self.assertTrue(self.api.top_navigation(self.request))
        self.assertEqual(
            len(json.loads(self.api.top_navigation(self.request))),
            0
        )


class TestAngularJsPortletNavigation(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.api = getUtility(IRestApi)

    def test_empty_navigation(self):
        self.assertEqual(
            json.loads(self.api.navigation_tree(self.request)),
            []
        )

    def test_folder_in_navigation(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')

        self.assertTrue(self.api.navigation_tree(self.request))
        self.assertEqual(
            json.loads(self.api.navigation_tree(self.request)),
            [{
                u'id': u'folder1',
                u'title': u'Folder 1',
                u'description': u'',
                u'url': 'folder1',
                u'children': []
            }]
        )

    def test_multiple_folders_in_navigation(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.invokeFactory('Folder', 'folder2', title='Folder 2')

        self.assertTrue(self.api.navigation_tree(self.request))
        self.assertEqual(
            len(json.loads(self.api.navigation_tree(self.request))), 2
        )
        self.assertEqual(
            [
                x['id'] for x
                in json.loads(self.api.navigation_tree(self.request))
            ],
            ['folder1', 'folder2']
        )

    def test_do_not_show_excluded_from_nav_folder(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.exclude_from_nav = True
        self.portal.folder1.reindexObject(idxs=['exclude_from_nav'])

        self.assertEqual(
            len(json.loads(self.api.navigation_tree(self.request))),
            0
        )

    def test_show_nested_folder_in_navigation(self):
        self.request.set('path', '/folder1')
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.invokeFactory(
            'Folder', 'folder2', title='Folder 2'
        )

        self.assertEqual(
            json.loads(self.api.navigation_tree(self.request))[0]['id'],
            'folder1'
        )
        self.assertEqual(
            json.loads(
                self.api.navigation_tree(
                    self.request
                )
            )[0]['children'][0]['id'],
            'folder2'
        )
