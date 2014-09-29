# -*- coding: utf-8 -*-
from Acquisition import aq_chain
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from plone.app.angularjs.interfaces import IRestApi

import json


DEBUG = False


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


def json_api_call(func):
    """ decorator to return all values as json
    """
    def decorator(*args, **kwargs):
        instance = args[0]
        request = getattr(instance, 'request', None)
        request.response.setHeader(
            'Content-Type',
            'application/json; charset=utf-8'
        )
        result = func(*args, **kwargs)
        return json.dumps(result, indent=2, sort_keys=True)

    return decorator


class Traversal(BrowserView):

    @json_api_call
    def __call__(self):
        portal = getSite()
        path = self.request.get('path')
        if not path:
            return {
                'code': '404',
                'message': "No path has been provided.",
            }
        path = '/'.join(portal.getPhysicalPath()) + '/' + path
        try:
            obj = portal.restrictedTraverse(path)
        except KeyError:
            return {
                'code': '404',
                'message': "No object found for path '%s'." % path,
            }
        try:
            text = obj.getText()
        except AttributeError:
            text = ''
        return {
            'route': path,
            'id': obj.id,
            'title': obj.title,
            'description': obj.Description(),
            'text': text
        }


class TopNavigation(BrowserView):

    @json_api_call
    def __call__(self):
        portal = getSite()
        catalog = getToolByName(portal, 'portal_catalog')
        portal_path = '/'.join(portal.getPhysicalPath())
        return [
            {
                'id': brain.id,
                'title': brain.Title,
                'description': brain.description,
                'path': brain.getPath().replace(
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


class PortletNavigation(BrowserView):

    @json_api_call
    def __call__(self):
        portal = getSite()
        catalog = getToolByName(portal, 'portal_catalog')
        portal_path = '/'.join(portal.getPhysicalPath())

        top_level_children = [
            {
                'id': brain.id,
                'title': brain.Title,
                'description': brain.description,
                'path': brain.getPath().replace(
                    portal_path, ''
                ).lstrip('/'),
                'children': []
            }
            for brain in catalog(
                {
                    'path': {'query': portal_path, 'depth': 1},
                    'sort_on': 'getObjPositionInParent',
                }
            ) if brain.exclude_from_nav is not True
        ]

        path = self.request.get('path')
        if path:
            try:
                obj = portal.restrictedTraverse(portal_path + path)
            except KeyError:
                pass
            if obj:
                chain = aq_chain(obj)[:-3]
                output = []
                # begin with the children of the object that has been selected
                for child in chain[0].objectItems():
                    output.append({
                        'id': child[1].id,
                        'title': child[1].title,
                        'description': child[1].description,
                        'path': '/'.join(child[1].getPhysicalPath()[2:]),
                        'children': []
                    })
                # traverse the acquisition chain
                for item in chain:
                    output = [{
                        'id': item.id,
                        'title': item.title,
                        'description': item.description,
                        'path': '/'.join(item.getPhysicalPath()[2:]),
                        'children': output
                    }]
                # replace top level children with the one from aq_chain
                i = 0
                for child in top_level_children:
                    if child['id'] == item.id:
                        top_level_children[i] = output[0]
                    i = i + 1
        if DEBUG:
            print('')
            print('---------------')
            print('Navigation Tree')
            print('---------------')
            print(path)
            print('---------------')
            for item in top_level_children:
                print('+- ' + item['id'])
                for item in item['children']:
                    print('   +- ' + item['id'])
                    for item in item['children']:
                        print('      +- ' + item['id'])
            print('---------------')

        return top_level_children
