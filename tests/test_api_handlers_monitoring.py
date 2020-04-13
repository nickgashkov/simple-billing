from aiohttp.test_utils import TestClient


async def test_api_handlers_monitoring_returns_healthy_response(
        cli: TestClient,
) -> None:
    response = await cli.get('/healthcheck')
    response_json = await response.json()

    assert response_json == {'healthy': True}
