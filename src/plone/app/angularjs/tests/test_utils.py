# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.app.angularjs.utils import underscore_to_camelcase


class UnderscoreToCamelcaseUnitTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(underscore_to_camelcase(''), '')

    def test_simple_term(self):
        self.assertEqual(underscore_to_camelcase('lorem'), 'Lorem')

    def test_two_simple_terms(self):
        self.assertEqual(underscore_to_camelcase('lorem_ipsum'), 'LoremIpsum')
