# -*- coding: utf-8 -*-
from zope.interface import Interface


class IAPIRequest(Interface):
    """Marker for API requests.
    """


class IAPIMethod(Interface):
    """Marker for API methods. This allows us to auto-generate our API docs.
    """
