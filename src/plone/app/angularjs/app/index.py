from zope.site.hooks import getSite
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AngularAppRootView(BrowserView):

    template = ViewPageTemplateFile('index.html')

    def __call__(self):
        return self.template()

    def base(self):
        """Return the portal url with a trailing '/'. Without this the Angular
           app won't work properly.
        """
        portal = getSite()
        return portal.absolute_url() + '/'
