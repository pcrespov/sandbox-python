import connexion
import six

from swagger_server.models.document import Document  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server import util


def docs_doc_id_get(doc_id):  # noqa: E501
    """docs_doc_id_get

    Gets document # noqa: E501

    :param doc_id: 
    :type doc_id: int

    :rtype: None
    """
    return 'do some magic!'


def set_document(doc_id, document=None):  # noqa: E501
    """set_document

    Set document # noqa: E501

    :param doc_id: 
    :type doc_id: int
    :param document: 
    :type document: dict | bytes

    :rtype: InlineResponse2002
    """
    if connexion.request.is_json:
        document = Document.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
