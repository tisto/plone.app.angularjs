# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView

import json


class AngularJsTopNavigation(BrowserView):

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_path = '/'.join(self.context.getPhysicalPath())
        return json.dumps(
            [
                {
                    'id': brain.id,
                    'title': brain.Title,
                    'description': brain.description,
                    'url': 'index.html' + brain.getPath().replace(
                        portal_path, ''
                    )
                }
                for brain in catalog({
                    'path': {
                        'query': '/'.join(self.context.getPhysicalPath()),
                        'depth': 1
                    },
                    'portal_type': 'Folder',
                    'sort_on': 'getObjPositionInParent'
                }) if brain.exclude_from_nav is not True
            ]
        )


class AngularJsPortletNavigation(BrowserView):

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_path = '/'.join(self.context.getPhysicalPath())

        def _get_children(context):
            return [
                {
                    'id': brain.id,
                    'title': brain.Title,
                    'description': brain.description,
                    'url': 'index.html' + brain.getPath().replace(
                        portal_path, ''
                    ),
                    'children': []
                } for brain in catalog({
                    'path': {'query': context.getPath(), 'depth': 1},
                    'sort_on': 'getObjPositionInParent',
                    }
                ) if brain.exclude_from_nav is not True
            ]
        return json.dumps(
            [
                {
                    'id': brain.id,
                    'title': brain.Title,
                    'description': brain.description,
                    'url': 'index.html' + brain.getPath().replace(
                        portal_path, ''
                    ),
                    'children': _get_children(brain)
                }
                for brain in catalog(
                    {
                        'path': {'query': portal_path, 'depth': 1},
                        'portal_type': 'Folder',
                        'sort_on': 'getObjPositionInParent',
                    }
                ) if brain.exclude_from_nav is not True
            ]
        )
