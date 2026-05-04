from clients.base_api_client import BaseApiClient
import requests
from typing import Final, Optional

ENDPOINT_POSTS: Final[str] = '/posts'

class WordPressApiClient(BaseApiClient):
    """Класс для работы с WordPress API"""
    def create_post(self, title: str | None = None, status: str = 'draft', content: str = '') -> requests.Response:
        payload = {'status': status, 'content': content}

        if title is not None:
            payload['title'] = title

        return self.post(ENDPOINT_POSTS, json=payload)

    def update_post(self, post_id: int, title: str, content: str = '') -> requests.Response:
        payload = {'title': title, 'content': content}

        return self.post(f'{ENDPOINT_POSTS}/{post_id}', json=payload)

    def delete_post(self, post_id: int, force: bool = True) -> requests.Response:
        params = {'force': force}

        return self.delete(f'{ENDPOINT_POSTS}/{post_id}', params=params)
