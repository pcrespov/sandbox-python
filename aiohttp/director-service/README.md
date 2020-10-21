# ``director`` service

Specification first rest-api project including client and server side

- [ ] TODO: systematic implementation of models and controllers using swagger-generator?

## Content

- ``director`` is a service application with an http-API
    - ``.opeanapi`` [OAS]
    - ``client-sdk`` client-side python sdk to interact with ``director`` service API
    - ``server`` service that offers an http-API



```bash

make clean
make .venv
source .venv/bin/activate

cd director-servec/client-sdk

# install all dependencies including those for testing
pip install -e ".[test]"

pip list | grep director
```


Run test and drop to PDB on first failure

```bash
pytest -s -x --pdb .

```


[OAS]:https://github.com/OAI/OpenAPI-Specification