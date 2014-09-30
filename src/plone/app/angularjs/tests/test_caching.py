# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

from plone.app.angularjs.testing import \
    PLONE_APP_ANGULARJS_WITH_CACHING_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser


class TestCaching(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_WITH_CACHING_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_js_caching(self):
        self.browser.open(
            self.portal_url + '/++theme++plone.app.angularjs/scripts/app.js'
        )

        self.assertEqual(
            'plone.resource',
            self.browser.headers['X-Cache-Rule'],
            'JS Resources are not cached.'
        )
        self.assertEqual(
            'plone.app.caching.strongCaching',
            self.browser.headers['X-Cache-Operation']
        )

    def test_css_caching(self):
        self.browser.open(
            self.portal_url + '/++theme++plone.app.angularjs/' +
            'bower_components/bootstrap/dist/css/bootstrap.min.css'
        )

        self.assertEqual(
            'plone.resource',
            self.browser.headers['X-Cache-Rule'],
            'CSS Resources are not cached.'
        )
        self.assertEqual(
            'plone.app.caching.strongCaching',
            self.browser.headers['X-Cache-Operation']
        )

    def test_index_html_templates_caching(self):
        self.browser.open(
            self.portal_url + '/index.html'
        )

        self.assertEqual(
            'plone.resource',
            self.browser.headers['X-Cache-Rule'],
            'HTML Templates are not cached.'
        )
        self.assertEqual(
            'plone.app.caching.strongCaching',
            self.browser.headers['X-Cache-Operation']
        )

    @unittest.skip('Not implemented yet')
    def test_html_templates_caching(self):
        self.browser.open(
            self.portal_url + '/navigation.tpl.html'
        )

        self.assertEqual(
            'plone.resource',
            self.browser.headers['X-Cache-Rule'],
            'HTML Templates are not cached.'
        )
        self.assertEqual(
            'plone.app.caching.strongCaching',
            self.browser.headers['X-Cache-Operation']
        )

    def test_api_methods_caching(self):
        self.browser.open(
            self.portal_url + '/++api++v1/top_navigation'
        )

        self.assertEqual(
            'plone.resource',
            self.browser.headers.get('X-Cache-Rule'),
            "Response header should have contained 'X-Cache-Rule' but did not."
        )
        self.assertEqual(
            'plone.app.caching.strongCaching',
            self.browser.headers.get('X-Cache-Operation')
        )
