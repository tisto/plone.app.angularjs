# -*- coding: utf-8 -*-
from zope.component import getUtility

from plone.app.angularjs.interfaces import IRestApi
from plone.app.angularjs.api.traverser import IAPIRequest
from plone.app.angularjs.testing import \
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter

import unittest2 as unittest
import json


class TestRestApiTraversalMethod(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.api = getUtility(IRestApi)

    def test_traversal_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal, self.request),
            name=""
        )
        self.assertTrue(
            view.publishTraverse(self.request, u"api")
        )

    def test_traversal_without_param(self):
        view = getMultiAdapter(
            (self.portal, self.request),
            name=""
        )
        self.assertTrue(
            view.publishTraverse(self.request, u"api")
        )
        view.publishTraverse(self.request, u"api").traverse(
            'v1',
            ''
        )
        self.assertTrue(IAPIRequest.providedBy(self.request))

    def test_traversal_empty_param(self):
        self.assertFalse(self.api.traversal(self.request))

    def test_traversal_not_found(self):
        self.request.set('path', 'nonexistingdoc')
        self.assertEqual(
            json.loads(self.api.traversal(self.request)),
            {'title': 'Object not found.'}
        )

    def test_traversal_document(self):
        self.portal.invokeFactory('Document', 'doc1')
        self.request.set('path', 'doc1')

        self.assertEqual(
            json.loads(self.api.traversal(self.request)),
            {
                u'route': u'/plone/doc1',
                u'title': u'',
                u'description': u'',
                u'text': u'',
                u'id': u'doc1'
            }
        )

    def test_traversal_document_sets_title(self):
        self.portal.invokeFactory('Document', 'doc1', title=u'Document 1')
        self.request.set('path', 'doc1')

        self.assertEqual(
            json.loads(self.api.traversal(self.request)),
            {
                u'route': u'/plone/doc1',
                u'title': u'Document 1',
                u'description': u'',
                u'text': u'',
                u'id': u'doc1'
            }
        )

    def test_traversal_document_sets_description(self):
        self.portal.invokeFactory('Document', 'doc1', title=u'Document 1')
        self.portal.doc1.setDescription(u'I am the first document!')
        self.request.set('path', 'doc1')

        self.assertTrue(self.api.traversal(self.request))
        self.assertEqual(
            json.loads(self.api.traversal(self.request)),
            {
                u'route': u'/plone/doc1',
                u'title': u'Document 1',
                u'description': u'I am the first document!',
                u'text': u'',
                u'id': u'doc1'
            }
        )

    def test_traversal_folder(self):
        self.portal.invokeFactory('Folder', 'folder1')
        self.request.set('path', 'folder1')

        self.assertEqual(
            json.loads(self.api.traversal(self.request)),
            {
                u'route': u'/plone/folder1',
                u'title': u'',
                u'description': u'',
                u'text': u'',
                u'id': u'folder1'
            }
        )

    def test_traversal_nested_document(self):
        self.portal.invokeFactory('Folder', 'folder1')
        self.portal.folder1.invokeFactory('Document', 'doc1')
        self.request.set('path', 'folder1/doc1')

        self.assertEqual(
            json.loads(self.api.traversal(self.request)),
            {
                u'route': u'/plone/folder1/doc1',
                u'title': u'',
                u'description': u'',
                u'text': u'',
                u'id': u'doc1'
            }
        )
