import connexion
import six

from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.registration_data import RegistrationData  # noqa: E501
from swagger_server import util


def confirm_token_post(token):  # noqa: E501
    """Confirms some operation by given user

    E.g. to confirm account, password reset, etc. Token encrypts user and action to be confirmed # noqa: E501

    :param token: Confirmation token encoding idenfitier and operation to confirm
    :type token: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        token = .from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def login_post():  # noqa: E501
    """Logs client into the service

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def logout_post():  # noqa: E501
    """logout_post

    Logs out client from the service # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def me_get():  # noqa: E501
    """Base entry-point for current API client&#39;s information

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def register_post(body):  # noqa: E501
    """Registers new user

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = RegistrationData.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
