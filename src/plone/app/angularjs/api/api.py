# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from plone.app.angularjs.interfaces import IRestApi

import json


class ApiOverview(BrowserView):

    template = ViewPageTemplateFile('api.pt')

    def __call__(self):
        return self.template()

    def api_methods(self):
        portal_url = getSite().absolute_url()
        return [
            {
                'id': x,
                'description': IRestApi.get(x).getDoc(),
                'url': '%s/++api++v1/%s' % (portal_url, x),
            } for x in IRestApi.names()
        ]


class RestApi(object):
    implements(IRestApi)

    def traversal(self, request):
        portal = getSite()
        path = request.get('path')
        if not path:
            return
        path = '/'.join(portal.getPhysicalPath()) + '/' + path
        try:
            obj = portal.restrictedTraverse(path)
        except KeyError:
            return json.dumps({'title': 'Object not found.'})
        try:
            text = obj.getText()
        except AttributeError:
            text = ''
        request.response.setHeader("Content-Type", "application/json")
        return json.dumps({
            'route': path,
            'id': obj.id,
            'title': obj.title,
            'description': obj.Description(),
            'text': text
        })

    def top_navigation(self, request):
        portal = getSite()
        catalog = getToolByName(portal, 'portal_catalog')
        portal_path = '/'.join(portal.getPhysicalPath())
        return json.dumps(
            [
                {
                    'id': brain.id,
                    'title': brain.Title,
                    'description': brain.description,
                    'url': brain.getPath().replace(
                        portal_path, ''
                    ).lstrip('/')
                }
                for brain in catalog({
                    'path': {
                        'query': '/'.join(portal.getPhysicalPath()),
                        'depth': 1
                    },
                    'portal_type': 'Folder',
                    'sort_on': 'getObjPositionInParent'
                }) if brain.exclude_from_nav is not True
            ]
        )

    def navigation_tree(self, request):
        portal = getSite()
        catalog = getToolByName(portal, 'portal_catalog')
        portal_path = '/'.join(portal.getPhysicalPath())

        def _get_children(context):
            return [
                {
                    'id': brain.id,
                    'title': brain.Title,
                    'description': brain.description,
                    'url': brain.getPath().replace(
                        portal_path, ''
                    ).lstrip('/'),
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
                    'url': brain.getPath().replace(
                        portal_path, ''
                    ).lstrip('/'),
                    'children': _get_children(brain)
                }
                for brain in catalog(
                    {
                        'path': {'query': portal_path, 'depth': 1},
                        'sort_on': 'getObjPositionInParent',
                    }
                ) if brain.exclude_from_nav is not True
            ]
        )
