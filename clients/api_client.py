"""Клиент для работы с WordPress API"""

from typing import Final, Optional

import requests

from clients.base_api_client import BaseApiClient

ENDPOINT_POSTS: Final[str] = "/posts"


class WordPressApiClient(BaseApiClient):
    """Класс для работы с WordPress API"""

    def create_post(
        self, title: Optional[str] = None, status: str = "draft", content: str = ""
    ) -> requests.Response:
        """Создает пост"""
        payload = {"status": status, "content": content}

        if title is not None:
            payload["title"] = title

        return self.post(ENDPOINT_POSTS, json=payload)

    def update_post(
        self, post_id: int, title: str, content: str = ""
    ) -> requests.Response:
        """Обновляет пост"""
        payload = {"title": title, "content": content}

        return self.post(f"{ENDPOINT_POSTS}/{post_id}", json=payload)

    def delete_post(self, post_id: int, force: bool = True) -> requests.Response:
        """Удаляет пост"""
        params = {"force": force}

        return self.delete(f"{ENDPOINT_POSTS}/{post_id}", params=params)

    def get_post(self, post_id: int) -> requests.Response:
        """Получает пост по ID"""
        return self.get(f"{ENDPOINT_POSTS}/{post_id}")

    def get_posts_list(
        self, status: Optional[str] = None, search: Optional[str] = None
    ) -> requests.Response:
        """Получает список постов с фильтрацией"""
        params = {}

        if status:
            params["status"] = status
        if search:
            params["search"] = search

        return self.get(ENDPOINT_POSTS, params=params)
