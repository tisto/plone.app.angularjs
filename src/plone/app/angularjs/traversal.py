# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.component import adapts
from plone.dexterity.interfaces import IDexterityItem
from zope.publisher.interfaces.browser import IBrowserRequest
from plone.app.angularjs.app.index import AngularAppRootView
from plone.app.angularjs.api.traverser import IAPIRequest
from plone.app.angularjs.api.api import ApiOverview
import json


class AngularAppPortalRootTraverser(DefaultPublishTraverse):
    adapts(IPloneSiteRoot, IBrowserRequest)

    def publishTraverse(self, request, name):
        if IAPIRequest.providedBy(request):
            if name == '' or name == 'folder_listing' or name == 'front-page':
                return ApiOverview(self.context, self.request)
            if name == 'traversal':
                from plone.app.angularjs.api.api import Traversal
                return Traversal(self.context, self.request)
            if name == 'top_navigation':
                from plone.app.angularjs.api.api import TopNavigation
                return TopNavigation(self.context, self.request)
            if name == 'portlet_navigation':
                from plone.app.angularjs.api.api import PortletNavigation
                return PortletNavigation(self.context, self.request)
            return json.dumps({
                'code': '404',
                'message': "API method '%s' not found." % name,
            })
        is_front_page = request.URL.endswith('front-page')
        no_front_page = \
            request.URL.endswith('folder_listing') or \
            request.URL.endswith('folder_contents')
        if is_front_page or no_front_page:
            # stop traversing
            request['TraversalRequestNameStack'] = []
            # return angular app view
            return AngularAppRootView(self.context, self.request)()
        return super(AngularAppPortalRootTraverser, self).publishTraverse(
            request,
            name
        )


class AngularAppRedirectorTraverser(DefaultPublishTraverse):
    adapts(IDexterityItem, IBrowserRequest)
    # XXX: Adapting IContentish works only for Archetypes content objects:
    # from Products.CMFCore.interfaces import IContentish
    # adapts(IContentish, IBrowserRequest)
    #
    # XXX: Adapting to IDexterityContent collides with the traversal in
    # plone.dexterity/plone/dexterity/browser/traversal.py

    def publishTraverse(self, request, name):
        if not IPloneSiteRoot.providedBy(self.context):
            # stop traversing
            request['TraversalRequestNameStack'] = []
            # return angular app view
            return AngularAppRootView(self.context, self.request)()
        return super(AngularAppRedirectorTraverser, self).publishTraverse(
            request,
            name
        )
