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
                    'url': '#' + brain.getPath().replace(portal_path, '')
                }
                for brain in catalog(path='/')
            ]
        )


class AngularJsPortletNavigation(BrowserView):

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_path = '/'.join(self.context.getPhysicalPath())
        return json.dumps(
            [
                {
                    'id': brain.id,
                    'title': brain.Title,
                    'description': brain.description,
                    'url': '#' + brain.getPath().replace(portal_path, '')
                }
                for brain in catalog(path='/')
            ]
        )
