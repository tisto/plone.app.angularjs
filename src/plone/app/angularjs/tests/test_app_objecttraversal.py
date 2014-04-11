# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter


from plone.app.angularjs.testing import\
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING

import json


class TestObjectTraversal(unittest.TestCase):

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
                name="angularjs-object-traversal"
            )
        )

    def test_object_traversal_without_param(self):
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-object-traversal"
        )
        view = view.__of__(self.portal)
        self.assertFalse(view())

    def test_object_traversal_empty_param(self):
        self.request.set('object-traversal-path', '')
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-object-traversal"
        )
        view = view.__of__(self.portal)
        self.assertFalse(view())

    def test_object_traversal_document(self):
        self.portal.invokeFactory('Document', 'doc1')
        self.request.set('object-traversal-path', 'doc1')
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-object-traversal"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(
            json.loads(view()),
            {
                u'route': u'/plone/doc1',
                u'title': u'',
                u'description': u'',
                u'text': u'',
                u'id': u'doc1'
            }
        )

    def test_object_traversal_document_sets_title(self):
        self.portal.invokeFactory('Document', 'doc1', title=u'Document 1')
        self.request.set('object-traversal-path', 'doc1')
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-object-traversal"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(
            json.loads(view()),
            {
                u'route': u'/plone/doc1',
                u'title': u'Document 1',
                u'description': u'',
                u'text': u'',
                u'id': u'doc1'
            }
        )

    def test_object_traversal_document_sets_description(self):
        self.portal.invokeFactory('Document', 'doc1', title=u'Document 1')
        self.portal.doc1.setDescription(u'I am the first document!')
        self.request.set('object-traversal-path', 'doc1')
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-object-traversal"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(
            json.loads(view()),
            {
                u'route': u'/plone/doc1',
                u'title': u'Document 1',
                u'description': u'I am the first document!',
                u'text': u'',
                u'id': u'doc1'
            }
        )

    def test_object_traversal_folder(self):
        self.portal.invokeFactory('Folder', 'folder1')
        self.request.set('object-traversal-path', 'folder1')
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-object-traversal"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(
            json.loads(view()),
            {
                u'route': u'/plone/folder1',
                u'title': u'',
                u'description': u'',
                u'text': u'',
                u'id': u'folder1'
            }
        )

    def test_object_traversal_nested_document(self):
        self.portal.invokeFactory('Folder', 'folder1')
        self.portal.folder1.invokeFactory('Document', 'doc1')
        self.request.set('object-traversal-path', 'folder1/doc1')
        view = getMultiAdapter(
            (self.portal, self.request),
            name="angularjs-object-traversal"
        )
        view = view.__of__(self.portal)

        self.assertTrue(view())
        self.assertEqual(
            json.loads(view()),
            {
                u'route': u'/plone/folder1/doc1',
                u'title': u'',
                u'description': u'',
                u'text': u'',
                u'id': u'doc1'
            }
        )
