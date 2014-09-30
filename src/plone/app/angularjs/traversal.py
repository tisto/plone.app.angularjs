# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZPublisher.BaseRequest import DefaultPublishTraverse
from plone.dexterity.interfaces import IDexterityItem
from plone.app.angularjs.interfaces import IAPIRequest
from plone.app.angularjs.api.api import ApiOverview
from zope.interface import implementer
from zope.interface import alsoProvides
from zope.component import adapter
from zope.component import adapts
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces.browser import IBrowserRequest

from zope.site.hooks import getSite

import json


class AngularAppRootView(BrowserView):

    template = ViewPageTemplateFile('app/index.html')

    def __call__(self):
        return self.template()

    def base(self):
        """Return the portal url with a trailing '/'. Without this the Angular
           app won't work properly.
        """
        portal = getSite()
        return portal.absolute_url() + '/'


@adapter(IPloneSiteRoot, IHTTPRequest)
@implementer(ITraversable)
class APITraverser(object):
    """The root API traverser
    """

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, postpath):
        alsoProvides(self.request, IAPIRequest)
        return self.context


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
