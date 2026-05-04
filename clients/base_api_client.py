from config import WP_API_URL, WP_API_USER, WP_API_PASS
import requests

class BaseApiClient:
    """Базовый API класс"""
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.auth = (WP_API_USER, WP_API_PASS)
        self.base_url = f'{WP_API_URL}/index.php?rest_route=/wp/v2'

    def _build_url(self, endpoint: str) -> str:
        return f'{self.base_url}{endpoint}'

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.session.post(self._build_url(endpoint), **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.session.delete(self._build_url(endpoint), **kwargs)
