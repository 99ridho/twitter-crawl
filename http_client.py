from aiohttp import (ClientResponse, ClientSession)
from typing import (Dict, Optional, Any)

class HTTPRequestData:
    def __init__(self, base_url: str, path: str, method: str, params: Dict[str, any] = {}, headers: Dict[str, str] = {}):
        self.base_url = base_url
        self.path = path
        self.method = method
        self.params = params
        self.headers = headers

class HTTPClient:
    async def request(self, data: HTTPRequestData) -> Optional[Any]:
        async with ClientSession() as session:
            method_lowercased = data.method.lower()
            url = data.base_url + data.path

            if method_lowercased == 'get':
                async with session.get(url, params=data.params, headers=data.headers) as resp:
                    return await resp.json()
            elif method_lowercased == 'post':
                async with session.post(url, params=data.params, headers=data.headers) as resp:
                    return await resp.json()
            elif method_lowercased == 'put':
                async with session.put(url, params=data.params, headers=data.headers) as resp:
                    return await resp.json()
            elif method_lowercased == 'patch':
                async with session.patch(url, params=data.params, headers=data.headers) as resp:
                    return await resp.json()
            elif method_lowercased == 'delete':
                async with session.delete(url, params=data.params, headers=data.headers) as resp:
                    return await resp.json()
            else:
                return None