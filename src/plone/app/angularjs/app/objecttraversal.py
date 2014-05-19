# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces import IFolderish
from zope.site.hooks import getSite

import json


class AngularJsObjectTraversal(BrowserView):

    def __call__(self):
        path = self.request.get('object-traversal-path')
        if not path:
            return
        path = '/'.join(self.context.getPhysicalPath()) + '/' + path
        try:
            obj = self.context.restrictedTraverse(path)
        except KeyError:
            return json.dumps({'title': 'Object not found.'})
        try:
            text = obj.getText()
        except AttributeError:
            text = ''
        self.request.response.setHeader("Content-Type", "application/json")
        # XXX: Just debugging
        if not getattr(obj, 'id', False):
            obj = getSite()
            print "Not found '%s'" % path
        if IFolderish.providedBy(obj):
            text = 'Folder View'
        return json.dumps({
            'route': path,
            'id': obj.id,
            'title': obj.title,
            'description': obj.Description(),
            'text': text
        })
