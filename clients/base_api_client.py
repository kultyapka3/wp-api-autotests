"""Базовый клиент API"""

from typing import Optional, Tuple, Dict

import requests


class BaseApiClient:
    """Базовый API класс"""

    def __init__(
        self,
        base_url: str,
        auth: Optional[Tuple[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url
        self.session = requests.Session()

        if auth:
            self.session.auth = auth

        if headers:
            self.session.headers.update(headers)

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET-запрос"""
        return self.session.get(self._build_url(endpoint), **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST-запрос"""
        return self.session.post(self._build_url(endpoint), **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE-запрос"""
        return self.session.delete(self._build_url(endpoint), **kwargs)
