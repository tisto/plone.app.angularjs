# -*- coding: utf-8 -*-
from plone.app.angularjs.testing import \
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import directlyProvides
from zope.component import getMultiAdapter

from plone.app.textfield.value import RichTextValue
from plone.app.angularjs.interfaces import IAPIRequest

import unittest2 as unittest
import json


class TestRestApiTraversalMethod(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        directlyProvides(self.portal, IAPIRequest)

    def test_traversal_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal, self.request),
            name="traversal"
        )
        self.assertTrue(view())

    def test_traversal_without_param(self):
        view = getMultiAdapter(
            (self.portal, self.request),
            name="traversal"
        )
        self.assertEqual(
            json.loads(view()),
            {u'message': u'No path has been provided.', u'code': u'404'}
        )

    def test_traversal_empty_param(self):
        self.request.set('path', '')
        view = getMultiAdapter(
            (self.portal, self.request),
            name="traversal"
        )
        self.assertEqual(
            json.loads(view()),
            {u'message': u'No path has been provided.', u'code': u'404'}
        )

    def test_traversal_not_found(self):
        self.request.set('path', 'nonexisting')

        view = getMultiAdapter(
            (self.portal, self.request),
            name="traversal"
        )

        self.assertEqual(
            json.loads(view()),
            {
                u'code': u'404',
                u'message': u"No object found for path '/plone/nonexisting'."
            }
        )

    def test_traversal_document(self):
        self.portal.invokeFactory('Document', 'doc1')
        self.portal.doc1.text = RichTextValue(
            u"Lorem ipsum.",
            'text/plain',
            'text/html'
        )
        self.request.set('path', 'doc1')

        view = getMultiAdapter(
            (self.portal, self.request),
            name="traversal"
        )

        self.assertEqual(
            json.loads(view()),
            {
                u'route': u'/plone/doc1',
                u'title': u'',
                u'description': u'',
                u'text': u'<p>Lorem ipsum.</p>',
                u'id': u'doc1'
            }
        )

    def test_traversal_document_sets_title(self):
        self.portal.invokeFactory('Document', 'doc1', title=u'Document 1')
        self.request.set('path', 'doc1')

        view = getMultiAdapter(
            (self.portal, self.request),
            name="traversal"
        )

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

    def test_traversal_document_sets_description(self):
        self.portal.invokeFactory('Document', 'doc1', title=u'Document 1')
        self.portal.doc1.setDescription(u'I am the first document!')
        self.request.set('path', 'doc1')

        view = getMultiAdapter(
            (self.portal, self.request),
            name="traversal"
        )

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

    def test_traversal_folder(self):
        self.portal.invokeFactory('Folder', 'folder1')
        self.request.set('path', 'folder1')

        view = getMultiAdapter(
            (self.portal, self.request),
            name="traversal"
        )

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

    def test_traversal_nested_document(self):
        self.portal.invokeFactory('Folder', 'folder1')
        self.portal.folder1.invokeFactory('Document', 'doc1')
        self.request.set('path', 'folder1/doc1')

        view = getMultiAdapter(
            (self.portal, self.request),
            name="traversal"
        )

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
