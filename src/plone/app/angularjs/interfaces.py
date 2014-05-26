from zope.interface import Interface


class IRestApi(Interface):
    """
    """

    def navigation_tree():
        """Returns the full portlet navigation tree.
        """

    def top_navigation():
        """Returns the top navigation entries.
        """
