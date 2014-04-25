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
# XXX: This interface is needed else we end up
# on the traverser of plone.app.imaging
# used for archetypes that implements .../image_<size_name>
from plone.app.imaging.interfaces import IBaseObject


class IAPIRequest(Interface):
    """Marker for API requests
    """


class FakeView(BrowserView):

    def __call__(self):
        self.request.response.setStatus(418)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps("I'm a teapot")


@adapter(IBaseObject, IAPIRequest)
class APIInnerTraverser(DefaultPublishTraverse):
    """Traverses the policy container
    """

    def publishTraverse(self, request, name):
        # TODO: WebDav here usually mangles a bit some variables in request
        # (like traversed stuff, etc) so the fake PUT or DELETE at the end
        # is removed
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

    def traverse(self, name, postpath):  # pylint: disable=unused-argument
        alsoProvides(self.request, IAPIRequest)
        return self.context
