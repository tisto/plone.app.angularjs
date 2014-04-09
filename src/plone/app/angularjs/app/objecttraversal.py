# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView

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
        return json.dumps({
            'route': path,
            'id': obj.id,
            'title': obj.title,
            'description': obj.Description(),
            'text': text
        })
