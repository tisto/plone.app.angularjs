from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.component import adapts
from Products.CMFCore.interfaces._content import IContentish
from zope.publisher.interfaces.browser import IBrowserRequest
from plone.app.angularjs.app.index import AngularAppRootView


class AngularAppPortalRootTraverser(DefaultPublishTraverse):
    adapts(IPloneSiteRoot, IBrowserRequest)

    def publishTraverse(self, request, name):
        is_front_page = request.URL.endswith('front-page')
        no_front_page = request.URL.endswith('folder_listing')
        if is_front_page or no_front_page:
            # stop traversing
            request['TraversalRequestNameStack'] = []
            # return angular app view
            return AngularAppRootView(self.context, self.request)()
        return DefaultPublishTraverse.publishTraverse(self, request, name)
        return super(AngularAppPortalRootTraverser, self).publishTraverse(
            request,
            name
        )


class AngularAppRedirectorTraverser(DefaultPublishTraverse):
    adapts(IContentish, IBrowserRequest)

    def publishTraverse(self, request, name):
        if not IPloneSiteRoot.providedBy(self.context):
            print "Return Angular App for %s" % self.request.URL
            # stop traversing
            request['TraversalRequestNameStack'] = []
            # return angular app view
            return AngularAppRootView(self.context, self.request)()
        return super(AngularAppRedirectorTraverser, self).publishTraverse(
            request,
            name
        )
