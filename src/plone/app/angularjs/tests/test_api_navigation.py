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
                u'label': u'Folder 1',
                u'description': u'',
                u'url': u'folder1',
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

    def test_show_top_level_siblings_in_navigation(self):
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.invokeFactory('Folder', 'folder2', title='Folder 2')
        self.portal.invokeFactory('Folder', 'folder3', title='Folder 3')

        self.assertEqual(
            len(json.loads(self.api.navigation_tree(self.request))),
            3
        )
        self.assertEqual(
            [
                x['id'] for x
                in json.loads(self.api.navigation_tree(self.request))
            ],
            ['folder1', 'folder2', 'folder3']
        )

    def test_show_top_level_siblings_in_navigation_with_nested(self):
        self.request.set('path', '/folder1')
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.invokeFactory('Folder', 'folder2', title='Folder 2')
        self.portal.invokeFactory('Folder', 'folder3', title='Folder 3')

        self.assertEqual(
            len(json.loads(self.api.navigation_tree(self.request))),
            3
        )

    def test_show_nested_folder_in_navigation(self):
        self.request.set('path', '/folder1/folder2')
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
        self.assertEqual(
            json.loads(
                self.api.navigation_tree(
                    self.request
                )
            )[0]['children'][0]['url'],
            'folder1/folder2'
        )

    def test_show_double_nested_folder_in_navigation(self):
        self.request.set('path', '/folder1/folder2/folder3')
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.folder1.invokeFactory(
            'Folder', 'folder2', title='Folder 2'
        )
        self.portal.folder1.folder2.invokeFactory(
            'Folder', 'folder3', title='Folder 3'
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
        self.assertEqual(
            json.loads(
                self.api.navigation_tree(
                    self.request
                )
            )[0]['children'][0]['children'][0]['id'],
            'folder3'
        )

    def test_show_nested_folder_in_navigation_and_top_level_items(self):
        # root
        # +- folder1
        # +- folder2
        # |  + folder2-1
        # +- folder3
        self.request.set('path', '/folder2/folder2-1')
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.portal.invokeFactory('Folder', 'folder2', title='Folder 2')
        self.portal.invokeFactory('Folder', 'folder3', title='Folder 3')
        self.portal.folder2.invokeFactory(
            'Folder', 'folder2-1', title='Folder 2-1'
        )

        self.assertEqual(
            json.loads(self.api.navigation_tree(self.request))[0]['id'],
            'folder1'
        )
        self.assertEqual(
            json.loads(self.api.navigation_tree(self.request))[1]['id'],
            'folder2'
        )
        self.assertEqual(
            json.loads(
                self.api.navigation_tree(
                    self.request
                )
            )[1]['children'][0]['id'],
            'folder2-1'
        )
        self.assertEqual(
            json.loads(self.api.navigation_tree(self.request))[2]['id'],
            'folder3'
        )

    def test_full(self):
        # root
        # +- front-page
        # +- news
        # |  + news1
        # +- events
        self.request.set('path', '/news')
        self.portal.invokeFactory('Folder', 'front-page', title='Front Page')
        self.portal.invokeFactory('Folder', 'news', title='News')
        self.portal.invokeFactory('Folder', 'events', title='Events')
        self.portal.news.invokeFactory(
            'Folder', 'news1', title='News 1'
        )

        self.assertEqual(
            json.loads(self.api.navigation_tree(self.request))[0]['id'],
            'front-page'
        )
        self.assertEqual(
            json.loads(self.api.navigation_tree(self.request))[1]['id'],
            'news'
        )
        self.assertEqual(
            json.loads(
                self.api.navigation_tree(
                    self.request
                )
            )[1]['children'][0]['id'],
            'news1'
        )
        self.assertEqual(
            json.loads(self.api.navigation_tree(self.request))[2]['id'],
            'events'
        )
