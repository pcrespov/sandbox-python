# aiohttp-samples

Playground with some samples of server/client apps based on aiohttp framework


- [ ] TODO: oath athentication?
- [ ] TODO: use [cookiecutter] to generate project. Check [cookiecutter-aiohttp-api](https://github.com/luizalabs/cookiecutter-aiohttp-api)


[cookiecutter]:https://github.com/audreyr/cookiecutter



# [aiohttp]

Async python web server

## docs

- [A good overview of asyncio](https://guillotina.readthedocs.io/en/latest/training/asyncio.html)
-

## tools

- [aiohttp-session]
- [aiohttp-security]
- [aiohttp-admin] builds an admin interface on top of an existing data-model
    - database agnostic
    - decoupled ORM
- [aiohhtp-login] Registration and authorization (including social) for aiohttp apps
- [guillotina] a full-feathred python asyncio rest resource application server
- [aio-manager](https://github.com/rrader/aio_manager)


## samples

- https://github.com/rrader/aiohttp-boilerplates
- git@github.com:embali/aiowing.git

[aiohttp]:https://aiohttp.readthedocs.io/en/stable/
[aiohttp-session]:http://aiohttp-session.readthedocs.io/en/latest/
[aiohttp-security]:https://aiohttp-security.readthedocs.io/en/latest/
[aiohhtp-login]:https://github.com/imbolc/aiohttp-login


# OpenAPI Specification language

[openapi] enable developers to design a technology-agnostic API interface that forms the basis of their API development and consumption

## docs

Lots of vague and non-conclusive discussions about REST APIs. Some articles I found
- [RESTful API Design Tips from Experience by Boyer](https://medium.com/studioarmix/learn-restful-api-design-ideals-c5ec915a430f)
- [Understanding REST and RPC for HTTP APIs by XX](https://www.smashingmagazine.com/2016/09/understanding-rest-and-rpc-for-http-apis/)

Handy manuals or references:
- [Best Practices in API Design by Swagger](https://swagger.io/resources/articles/best-practices-in-api-design/)  
- OpenAPI specs
   - [specs @ github](https://github.com/OAI/OpenAPI-Specification)
   - [specs @ swagger.io](https://swagger.io/docs/specification)
- [openapi and json-schema solved](https://philsturgeon.uk/api/2018/04/13/openapi-and-json-schema-divergence-solved/): deals with how to merge [json-schema] validations into [openapi] specifications
- Annotation and validators
    - [Rx] is a [yaml] and [json] validator
    - [json-schema]
- other REST specification languages
    - [dropbox-stone] has some published samples in [dropbpox-api-spec](https://github.com/dropbox/dropbox-api-spec)
    - [json-api]
    - [odata]


[dropbox-stone]:https://github.com/dropbox/stone
[json-schema]:http://json-schema.org
[openapi]:https://github.com/OAI/OpenAPI-Specification
[Rx]:https://github.com/rjbs/Rx
[yaml]:https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html
[json]:https://www.json.org
[odata]:https://www.odata.org/
[json-api]:http://jsonapi.org/

## tools

- [swagger integration tools](https://swagger.io/tools/open-source/open-source-integrations)
- [connexion] (see example with odm alquemy inside)
- [aiobravado]
- [aiohttp-apiset]
- [guillotina]
    - **pros**
        - cookiecutter to bootstrap an application
        - design by contract (uses [zope.interface])
        - configuration, content-types (using interfaces).
        - application: python package installed in your environment and add to your list of applications in config file. addons: installation login into a container
        - users(are given roles and groups)/[roles](https://guillotina.readthedocs.io/en/latest/developer/roles.html#roles)(=granted permissions)/groups(=granted roles)
    - **cons**
        - schema is defined in python and not using OSI. Not reusable on client side!
        - too opinionated

[aiobravado]:https://github.com/sjaensch/aiobravado
[connexion]:https://github.com/zalando/connexion
[aiohttp-apiset]:http://aiohttp-apiset.readthedocs.io/en/latest/
[aiohttp-admin]:http://aiohttp-admin.readthedocs.io/en/latest/
[zope]:http://www.zope.org/en/latest/
[zope.interface]:https://zopeinterface.readthedocs.io/en/latest/README.html
[guillotina]:https://guillotina.readthedocs.io/en/latest/

## samples

- [sendgrid OAS](https://github.com/sendgrid/sendgrid-oai)
- [github API-specs](https://developer.github.com/v3/) design doc
