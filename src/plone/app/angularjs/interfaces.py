from zope.interface import Interface


class IRestApi(Interface):
    """
    """

    def portlet_navigation():
        """Returns the portlet navigation tree.
        """

    def top_navigation():
        """Returns the top navigation entries.
        """
