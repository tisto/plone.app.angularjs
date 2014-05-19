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

    def publishTraverse(self, request, name):
        """Always return the Angular app when traversing to
        Plone/index.html/<path>.
        """
        # stop traversing
        request['TraversalRequestNameStack'] = []
        # always return the angular app root
        return self.template()
