import requests
from typing import Any, Dict, Iterable, Optional
from src.config import Config

BASE_URL = Config.BASE_URL
DEFAULT_TIMEOUT = Config.TIMEOUT
DEFAULT_HEADERS = Config.HEADERS
CHUNK_SIZE = Config.STREAM_CHUNK_SIZE

def get_json(
        url: str,
        params: Optional[Dict[str, any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = DEFAULT_TIMEOUT
    ) -> Dict[str, Any]:
    response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()

def get_stream(
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = DEFAULT_TIMEOUT
    ) -> Iterable[bytes]:
    response = requests.get(url=url, headers=headers, timeout=timeout, stream=True)
    response.raise_for_status()
    return response.iter_content(chunk_size=CHUNK_SIZE)

class Client:
    def __init__(
            self,
            base_url: str = BASE_URL,
            headers: Optional[Dict[str, str]] = None,
            timeout: float = DEFAULT_TIMEOUT
        ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = {**DEFAULT_HEADERS, **(headers or {})}
        self.timeout = timeout
        self.session = requests.Session()

    def close(self) -> None:
        self.session.close()

    def _url(self, url: str) -> str:
        return url if url.startswith("http") else f"{self.base_url}/{url.lstrip('/')}"

    # def get(self, endpoint, params=None):
    #     url = f"{self.base_url}/{endpoint}"
    #     response = self.session.get(url, params=params, timeout=self.timeout)
    #     response.raise_for_status()
    #     return response.json()

    def get_json(
            self,
            url: str,
            params: Optional[Dict[str, any]] = None,
            headers: Optional[Dict[str, str]] = None,
            timeout: float = DEFAULT_TIMEOUT
        ) -> Dict[str, Any]:
        response = self.session.get(url=url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def get_stream(
            self,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            timeout: float = DEFAULT_TIMEOUT
        ) -> Iterable[bytes]:
        response = self.session.get(url=url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()
        return response.iter_content(chunk_size=CHUNK_SIZE)

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()