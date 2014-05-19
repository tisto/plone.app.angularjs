from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zope.site.hooks import getSite
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AngularAppRootView(BrowserView):
    implements(IPublishTraverse)
    template = ViewPageTemplateFile('index.html')

    def __call__(self):
        return self.template()

    def base(self):
        portal = getSite()
        return '%s/%s' % (
            self.request.base,
            portal.id
        )


from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.http import IHTTPRequest
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFCore.interfaces import IContentish
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.component import adapts
from zope.publisher.interfaces import IRequest
from Products.CMFCore.interfaces._content import ISiteRoot


# https://github.com/collective/collective.routes/blob/master/collective/routes/traverser.py
class AngularAppTraverser(DefaultPublishTraverse):
    adapts(ISiteRoot, IRequest)

    def publishTraverse(self, request, name):
        return AngularAppRootView(self.context, self.request)()
        return DefaultPublishTraverse.publishTraverse(self, request, name)


# https://github.com/zopefoundation/Zope/blob/master/src/ZPublisher/BaseRequest.py#L320
@adapter(IPloneSiteRoot, IHTTPRequest)
@implementer(IPublishTraverse)
class AngularAppTraverser(object):

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        if IContentish.providedBy(self.context) or IPloneSiteRoot.providedBy(self.context):
            # stop traversing
            request['TraversalRequestNameStack'] = []
            # return angular app view
            return AngularAppRootView(self.context, self.request)()
