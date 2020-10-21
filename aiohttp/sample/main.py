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


# operationId-handler association
opmap = OperationIdMapping(
    **{'setDocument':set_document, 'api.root_get':api.root_get }
)


def main():
    router = SwaggerRouter(
        swagger_ui='/apidoc/',
        search_dirs=[BASE],
    )

    app = web.Application(
        router=router,
        middlewares=[jsonify],
    )

    # TODO: what is this??? Something to do with security!
    router.set_cors(app, domains='*', headers=(
        (hdrs.ACCESS_CONTROL_EXPOSE_HEADERS, hdrs.AUTHORIZATION),
    ))

    # Include our specifications in a router,
    # is now available in the swagger-ui to the address http://localhost:8080/swagger/?spec=v1
    router.include(
        spec='swagger.yaml',
        operationId_mapping=opmap,
        name='v1',  # name to access in swagger-ui
    )

    web.run_app(app)


if __name__ == '__main__':
    main()
