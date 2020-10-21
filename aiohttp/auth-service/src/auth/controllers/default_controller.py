import connexion
import six

from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server import util


def root_get():  # noqa: E501
    """Service health-check endpoint

    Some general information on the API and state of the service behind # noqa: E501


    :rtype: InlineResponse2001
    """
    return 'do some magic!'
