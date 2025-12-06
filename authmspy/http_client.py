from aiohttp import ClientSession

class HTTPClient:
    def __init__(self, base_url: str):
        self._session = ClientSession(
            base_url = base_url
        )
        
class DBHTTPClient(HTTPClient):
    async def send_post_request(self, endpoint_url: str, json: dict):
        async with self._session.post(
            url = endpoint_url,
            json = json
        ) as response:
            return await response.json()
        
    async def send_delete_request(self, endpoint_url, json):
        async with self._session.delete(
            url = endpoint_url,
            json = json
        ) as response:
            return await response.json()
        