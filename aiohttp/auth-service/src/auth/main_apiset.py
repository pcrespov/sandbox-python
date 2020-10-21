from pathlib import Path

from aiohttp import web, hdrs
from aiohttp_apiset import SwaggerRouter
from aiohttp_apiset.middlewares import jsonify
from aiohttp_apiset.swagger.operations import OperationIdMapping

BASE = Path(__file__).parent


DB = {}


def set_document(request, doc_id, body, errors):
    """ Simple handler for set document
    """
    if doc_id in DB:
        errors['doc_id'].add('Document already exists')

    if errors:
        raise errors

    body['doc_id'] = doc_id
    DB[doc_id] = body

    # dict response for jsonify middleware
    return body

# operationId-handler association
opmap = OperationIdMapping(
    setDocument=set_document
)

def main():
    router = SwaggerRouter(
        #search_dirs=[ BASE / ".." / ".." / ".openapi" ],
        swagger_ui='/thedoc/'
    )    
    
    pth = (BASE / ".." / ".." / ".openapi"/"swagger.yaml").resolve()
    router.include(str(pth))


    # router.add_post('/doc/{doc_id:\d+}', handler=set_document)

    app = web.Application(
        router=router,
        middlewares=[jsonify],
    )

    #router.set_cors(app, domains='*', headers=(
    #    (hdrs.ACCESS_CONTROL_EXPOSE_HEADERS, hdrs.AUTHORIZATION),
    #))


    # Include our specifications in a router,
    # is now available in the swagger-ui to the address http://localhost:8080/swagger/?spec=v1

    #router.include(
    #    spec='swagger.yaml',
    #    operationId_mapping=opmap,
    #    name='v1',  # name to access in swagger-ui
    #)

    web.run_app(app)


if __name__ == '__main__':
    main()
