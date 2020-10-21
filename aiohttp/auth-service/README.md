# authentication service

Demonstrates a very simple authentication service


- TODO: define authentication
- Handy to use [swaggerhub]'s editor and download *resolved YAML* 
  - better validation than vscode's extension `Swagger Viewer`
- Based on recommendations from
    - [RESTful API Design Tips from Experience by Boyer](https://medium.com/studioarmix/learn-restful-api-design-ideals-c5ec915a430f)
    - [Best Practices in API Design by Swagger](https://swagger.io/resources/articles/best-practices-in-api-design/)



## [oas3] notes
  - *Document Structure*: single/multiple with ``$ref``. Recommended root [oas3] document be named ``openapi.yaml``
  - *Data types*: 
   - primitive types(integer, number, string and boolean), w/ optional ``format`` modifier property (int32, int64, float, double, byte, binary, date, date-time, password)
    - ``null`` is **not** supported type (see nullable)
    - models defined using schemas
  - *Relative references in Uniform Resource Locators (URLs)* 
    - resolved using the URLs defined in the Server Object as a Base URI.
  - [oas3] document schema
  - Path Objects
    - Operation objects: skeleton of operation object ``GET`` on resources ``weather``:
      - Parameters objects
      - Responses objects    
    ```yaml
      paths:
        /weather:
          get:
            tags:
            summary:
            description:
            operationId:
            externalDocs:
            *parameters*:
            *responses*:
            deprecated:
            security:
            servers:
            requestBody:
            callbacks:
    ```
  - The Schema Object allows the definition of input and output data types. you store re-usable definitions that might appear in multiple places in your specification document/
  ```yaml
    components:
      schemas:
        [MyModel]:
          type:
          required:
          properties:
            [prop1]:
            [prop2]:
          
  ```




[oas3]:https://swagger.io/specification/

## Swagger/codegen notes

  - code generation tool dockerized. See ``.openapi/codegen.sh``
  - Response schemas should be references to ``definitions``, otherwise codegen will create automatically model for each with not very nice naming...


## Register user

```
POST /v1/register

// request
{
  "email": "end@@user.comx"
  "username": "foo"
  "password": "abc"
}


// response - 422
{
  "error": {
    "status": 422,
    "error": "FIELDS_VALIDATION_ERROR",
    "description": "One or more fields raised validation errors."
    "fields": {
      "email": "Invalid email address.",
      "password": "Password too short."
    }
  }
}

// response - 409
{
  "error": {
    "status": 409,
    "error": "EMAIL_ALREADY_EXISTS",
    "description": "An account already exists with this email."
  }
}

```


## Logging In

Registered user logs in and returns 
    - JWT access token for authenticating general requests
    - a new refresh token for requesting a new access token upon expiry     

```
POST /v1/login

// request
{
  "email": "end@@user.comx"
  "password": "abc"
}
```

## Renewing a Token
```
POST /v1/renew


// request
{
    "refresh token"
}

```

## Validating a Token

## Terminating a Session (logout)

## Authentication

- TODO: read [Stop using JWT for sessions](http://cryto.net/~joepie91/blog/2016/06/13/stop-using-jwt-for-sessions/)
- [JWT]
- Basic authentication: ``Authorization`` header stores token (i.e. uuid provided upon ``/login`` request).



[JWT]:https://en.wikipedia.org/wiki/JSON_Web_Token
[swaggerhub]:https://app.swaggerhub.com
[YAML]:https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html