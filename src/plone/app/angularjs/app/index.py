from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zope.site.hooks import getSite
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.component import adapts
from zope.publisher.interfaces import IRequest
from Products.CMFCore.interfaces._content import IContentish


class AngularAppRootView(BrowserView):
    implements(IPublishTraverse)
    template = ViewPageTemplateFile('index.html')

    def __call__(self):
        return self.template()

    def base(self):
        portal = getSite()
        return '%s/%s/' % (
            self.request.base,
            portal.id
        )


# https://github.com/collective/collective.routes/blob/master/collective/routes/traverser.py
# http://g0dil.de/wiki/PloneStuff
class AngularAppPortalRootTraverser(DefaultPublishTraverse):
    adapts(IPloneSiteRoot, IRequest)

    def publishTraverse(self, request, name):
        if request.URL == 'http://localhost:8080/Plone/folder_listing':
            # stop traversing
            request['TraversalRequestNameStack'] = []
            # return angular app view
            return AngularAppRootView(self.context, self.request)()
        return DefaultPublishTraverse.publishTraverse(self, request, name)


class AngularAppRedirectorTraverser(DefaultPublishTraverse):
    adapts(IContentish, IRequest)

    def publishTraverse(self, request, name):
        if not IPloneSiteRoot.providedBy(self.context):
            print "Return Angular App for %s" % self.request.URL
            # stop traversing
            request['TraversalRequestNameStack'] = []
            # return angular app view
            return AngularAppRootView(self.context, self.request)()
        return DefaultPublishTraverse.publishTraverse(self, request, name)
