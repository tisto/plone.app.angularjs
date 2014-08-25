# -*- coding: utf-8 -*-
from plone.app.angularjs.interfaces import IRestApi
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.angularjs.testing import\
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING
from zope.component import getUtility

import json
import unittest2 as unittest


class TestAngularJsFolderChildren(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.api = getUtility(IRestApi)

    def test_empty_navigation(self):
        self.assertEqual(
            json.loads(self.api.folder_children(self.request)),
            []
        )

    def test_folder_in_navigation(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')

        self.assertTrue(self.api.folder_children(self.request))
        self.assertEqual(
            json.loads(self.api.folder_children(self.request)),
            [{
                u'id': u'folder1',
                u'title': u'Folder 1',
                u'label': u'Folder 1',
                u'description': u'',
                u'url': '/plone/folder1',
                u'children': []
            }]
        )

    def test_do_not_show_excluded_from_nav_documents(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.exclude_from_nav = True
        self.portal.folder1.reindexObject(idxs=['exclude_from_nav'])

        self.assertEqual(
            len(json.loads(self.api.folder_children(self.request))),
            0
        )

    def test_folder_in_navigation_with_path(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.invokeFactory(
            'Folder', 'folder2', title='Folder 2')
        self.request.set('path', '/folder1')
        self.assertTrue(
            self.api.folder_children(self.request))
        self.assertEqual(
            json.loads(
                self.api.folder_children(self.request)
            ),
            [{
                u'id': u'folder2',
                u'title': u'Folder 2',
                u'label': u'Folder 2',
                u'description': u'',
                u'url': '/plone/folder1/folder2',
                u'children': []
            }]
        )

    def test_document_returns_parent_folder(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.invokeFactory(
            'Document', 'doc1', title='Document 1')
        self.request.set('path', '/folder1/doc1')
        self.assertTrue(
            self.api.folder_children(self.request))
        self.assertEqual(
            json.loads(
                self.api.folder_children(self.request)
            )[0]['id'],
            u'doc1'
        )
