import json
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import alsoProvides
from zope.component import adapter
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest
from ZPublisher.BaseRequest import DefaultPublishTraverse
from Products.Five.browser import BrowserView
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
# XXX: GAH
from plone.app.imaging.interfaces import IBaseObject


class IAPIRequest(Interface):
    """Marker for API requests
    """


class FakeView(BrowserView):

    def __call__(self):
        self.request.response.setStatus(413)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps("I'm a teapot")


@adapter(IBaseObject, IAPIRequest)
class APIInnerTraverser(DefaultPublishTraverse):
    """Traverses the policy container
    """

    def publishTraverse(self, request, name):
        if name in ('PUT', 'DELETE'):
            return FakeView(self.context, request)
        return super(APIInnerTraverser, self).publishTraverse(request, name)


@adapter(IPloneSiteRoot, IHTTPRequest)
@implementer(ITraversable)
class APITraverser(object):
    """The root API traverser
    """

    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, postpath): # pylint: disable=unused-argument
        alsoProvides(self.request, IAPIRequest)
        return self.context

