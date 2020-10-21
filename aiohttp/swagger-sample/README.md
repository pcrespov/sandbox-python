# swagger-sample

-  Uses https://app.swaggerhub.com/apis/pcrespov/test-simple/1.0.0 
-  Downloads auto-generated python client and flask server
- 


- [ ] TODO: dockerize all swagger generator tools. https://github.com/swagger-api/swagger-codegen
- [ ] TODO: aiohttp with async controlers??


## ``swagger_server``

-  [connexion] automatically maps the OpenAPI 2.0 Specification ([OAS]) defined in the ``swagger/swagger.yaml`` to python functions (see ``swagger_server.controller``)
-  [connection] validates input/outputs of all OAS calls 
    -  translates requests load into input parameters of controler functions
    -  returned values of controler functions are translated into json. probably using encoder
-  It runs on a flask server (but can also be aiohttp)


[connexion]:http://connexion.readthedocs.io/en/latest/
[flask]:http://flask.pocoo.org/
[OAS]:https://github.com/OAI/OpenAPI-Specification
