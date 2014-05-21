from zope.site.hooks import getSite
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AngularAppRootView(BrowserView):

    template = ViewPageTemplateFile('index.html')

    def __call__(self):
        return self.template()

    def base(self):
        portal = getSite()
        return '%s/%s/' % (
            self.request.base,
            portal.id
        )
