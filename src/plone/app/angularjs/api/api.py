# -*- coding: utf-8 -*-
from Acquisition import aq_chain
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

        top_level_children = [
            {
                'id': brain.id,
                'title': brain.Title,
                'label': brain.Title,
                'description': brain.description,
                'url': brain.getPath().replace(
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

        path = request.get('path')
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
                        'label': child[1].title,
                        'description': child[1].description,
                        'url': '/'.join(child[1].getPhysicalPath()[2:]),
                        'children': []
                    })
                # traverse the acquisition chain
                for item in chain:
                    output = [{
                        'id': item.id,
                        'title': item.title,
                        'label': item.title,
                        'description': item.description,
                        'url': '/'.join(item.getPhysicalPath()[2:]),
                        'children': output
                    }]
                # replace top level children with the one from aq_chain
                i = 0
                for child in top_level_children:
                    if child['id'] == item.id:
                        top_level_children[i] = output[0]
                    i = i + 1
        if True:
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

        return json.dumps(top_level_children)
