import aiohttp
import pytest
from pathlib import Path
import yaml


params = yaml.safe_load( Path("params.yml").read_text() )
assert params.get('deploys')

@pytest.mark.parametrize(
    "base_url, expected_display_name",
    [
        pytest.param(d['url'], d["display_name"]) for d in params["deploys"]
    ]
)
async def test_json_display_name(base_url: str, expected_display_name: str):
    url = f"{base_url}/static-frontend-data.json"
    async with aiohttp.ClientSession() as session, session.get(url) as response:
        assert response.status == 200, f"Failed to fetch URL: {url}"
        data = await response.json()

    assert data.get("displayName") == expected_display_name, f"Got {data}"
