import json

from aiohttp import web
from openapi_spec_validator import validate_spec_url

# Load the OpenAPI specification
with open("openapi.json") as f:
    spec = json.load(f)

# Create an Aiohttp application and define your routes
app = web.Application()


async def hello(request):
    return web.Response(text="Hello, world")


app.add_routes([web.get("/hello", hello)])


# Define a test function that validates the routes against the OpenAPI specification
def test_validate_routes():
    # Validate the routes against the OpenAPI specification
    errors = validate_spec_url(spec, app.router)

    # Check if there are any validation errors
    assert not errors, f"Validation errors: {errors}"
