# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.app.angularjs.utils import underscore_to_camelcase
from plone.app.angularjs.utils import get_object_schema
from plone.app.angularjs.utils import serialize_to_json
from plone.app.angularjs.testing import\
    PLONE_APP_ANGULARJS_INTEGRATION_TESTING
from plone.app.textfield.value import RichTextValue

from DateTime import DateTime


class SerializeToJsonIntegrationTest(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_serialize_title(self):
        self.portal.invokeFactory('Document', id='doc1', title='Doc 1')

        self.assertEqual(
            serialize_to_json(self.portal.doc1).get('title'),
            'Doc 1'
        )

    def test_serialize_description(self):
        self.portal.invokeFactory('Document', id='doc1', title='Doc 1')
        self.portal.doc1.description = u'Lorem Ipsum'

        self.assertEqual(
            serialize_to_json(self.portal.doc1).get('description'),
            'Lorem Ipsum'
        )

    def test_serialize_rich_text(self):
        self.portal.invokeFactory('Document', id='doc1', title='Doc 1')
        self.portal.doc1.text = RichTextValue(
            u"Lorem ipsum.",
            'text/plain',
            'text/html'
        )

        self.assertEqual(
            serialize_to_json(self.portal.doc1).get('text'),
            u'<p>Lorem ipsum.</p>'
        )

    def test_serialize_datetime(self):
        self.portal.invokeFactory('Document', id='doc1', title='Doc 1')
        self.portal.doc1.setEffectiveDate(DateTime('2014/04/04'))
        self.assertEqual(
            serialize_to_json(self.portal.doc1).get('effective'),
            '2014-04-04T00:00:00'
        )

    def test_ignore_underscore_values(self):
        self.portal.invokeFactory('Document', id='doc1', title='Doc 1')

        self.assertFalse(
            '__name__' in serialize_to_json(self.portal.doc1)
        )
        self.assertFalse(
            'manage_options' in serialize_to_json(self.portal.doc1)
        )


class GetObjectSchemaUnitTest(unittest.TestCase):

    layer = PLONE_APP_ANGULARJS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_document(self):
        self.portal.invokeFactory('Document', id='doc1', title='Doc 1')
        schema = [x[0] for x in get_object_schema(self.portal.doc1)]
        self.assertEqual(
            schema,
            [
                'title',
                'allow_discussion',
                'exclude_from_nav',
                'text',
                'relatedItems',
                'table_of_contents',
                'title',
                'meta_type',
                'isPrincipiaFolderish',
                'icon',
                'title',
                'meta_type',
                'isPrincipiaFolderish',
                'icon',
                'meta_type',
                'isPrincipiaFolderish',
                'title',
                'title',
                'allow_discussion',
                'exclude_from_nav',
                'rights',
                'contributors',
                'effective',
                'title',
                'expires',
                'language',
                'subjects',
                'creators',
                'description',
                'text',
                'relatedItems',
                'changeNote',
                'table_of_contents'
            ]
        )

    def test_folder(self):
        self.portal.invokeFactory('Folder', id='folder1', title='Folder 1')
        schema = [x[0] for x in get_object_schema(self.portal.folder1)]

        self.assertEqual(
            schema,
            [
                'title',
                'allow_discussion',
                'exclude_from_nav',
                'relatedItems',
                'nextPreviousEnabled',
                'title',
                'isAnObjectManager',
                'meta_type',
                'meta_types',
                'isPrincipiaFolderish',
                'icon',
                'isAnObjectManager',
                'meta_type',
                'meta_types',
                'isPrincipiaFolderish',
                'title',
                'meta_type',
                'isPrincipiaFolderish',
                'icon',
                'title',
                'meta_type',
                'isPrincipiaFolderish',
                'icon',
                'meta_type',
                'isPrincipiaFolderish',
                'title',
                'rights',
                'contributors',
                'effective',
                'title',
                'expires',
                'language',
                'subjects',
                'creators',
                'description',
                'title',
                'allow_discussion',
                'exclude_from_nav',
                'relatedItems',
                'nextPreviousEnabled'
            ]
        )


class UnderscoreToCamelcaseUnitTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(underscore_to_camelcase(''), '')

    def test_simple_term(self):
        self.assertEqual(underscore_to_camelcase('lorem'), 'Lorem')

    def test_two_simple_terms(self):
        self.assertEqual(underscore_to_camelcase('lorem_ipsum'), 'LoremIpsum')
