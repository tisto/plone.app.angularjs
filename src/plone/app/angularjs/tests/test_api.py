# -*- coding: utf-8 -*-
from plone.app.angularjs.traversal import IAPIRequest
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
import unittest2 as unittest

from zope.component import getMultiAdapter

from zope.interface import directlyProvides

from plone.app.angularjs.testing import\
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING

import json


class TestApi(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        directlyProvides(self.portal, IAPIRequest)

    def test_portlet_portlet_navigation_method(self):
        view = getMultiAdapter(
            (self.portal, self.request),
            name="portlet_navigation"
        )

        self.assertTrue(view())
        self.portal.invokeFactory('Folder', id='folder1', title='Folder 1')
        self.assertEqual(
            json.loads(view())[0]['path'],
            'folder1'
        )
        self.assertEqual(
            json.loads(view())[0]['id'],
            'folder1'
        )
        self.assertEqual(
            json.loads(view())[0]['path'],
            'folder1'
        )


class TestApiTraverser(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_named_adapter_api(self):
        view = getMultiAdapter(
            (self.portal, self.request),
            name=""
        )
        self.assertTrue(
            view.publishTraverse(self.request, u"api")
        )
        view.publishTraverse(self.request, u"api").traverse(
            'v1',
            '/news'
        )
        self.assertTrue(IAPIRequest.providedBy(self.request))
