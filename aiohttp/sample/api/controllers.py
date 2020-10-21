
from pathlib import Path

from aiohttp import web, hdrs
from aiohttp_apiset import SwaggerRouter
from aiohttp_apiset.middlewares import jsonify
from aiohttp_apiset.swagger.operations import OperationIdMapping


import api

BASE = Path(__file__).parent


DB = {}


async def set_document(request, doc_id, document, errors):
    """ Simple handler for set document
    :param request: aiohttp.web.Request
    :param errors: aiohttp_apiset.exceptions.ValidationError
                   optional param for manual raise validation errors
    :return: dict
    """
    if doc_id in DB:
        errors['doc_id'].add('Document already exists')

    if errors:
        raise errors

    document['doc_id'] = doc_id + 2
    DB[doc_id] = document

    # dict response for jsonify middleware
    return document


async def root_get():  # noqa: E501
    """Returns a nice greeting

    :rtype: str
    """
    greeting = "<h1>Hoi zaeme! Salut les d'jeunz!</h1><h3>This is {} responding!</h2>".format(__name__)
    return greeting


