from aiohttp import ClientSession

class HTTPClient:
    def __init__(self, base_url: str):
        self._session = ClientSession(
            base_url=base_url
        )
        
class DBHTTPClient(HTTPClient):
    async def send_post_request(self, endpoint: str, json: dict):
        async with self._session.post(
            url=f"http://127.0.0.1:4000/database/{endpoint}",
            json=json
        ) as response:
            return await response.json()
        