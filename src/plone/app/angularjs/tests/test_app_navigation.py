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
