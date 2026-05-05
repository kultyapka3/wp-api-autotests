"""Фикстуры для тестов"""

from typing import Iterator, Callable

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient


@pytest.fixture()
def api_client() -> WordPressApiClient:
    """Фикстура для API клиента"""
    return WordPressApiClient()


@pytest.fixture()
def db_client() -> WordPressDbClient:
    """Фикстура для БД клиента"""
    return WordPressDbClient()


@pytest.fixture()
def test_post_factory(db_client: WordPressDbClient) -> Iterator[Callable[[], int]]:
    """Создание тестового поста по вызову"""

    def _create() -> int:
        post_id = db_client.create_test_post(title="Test Title", content="Test Content")

        return post_id

    yield _create


@pytest.fixture(autouse=True)
def cleanup_test_posts(db_client: WordPressDbClient) -> Iterator[list[int]]:
    """Удаление созданных в тесте постов"""
    created_ids: list[int] = []
    yield created_ids

    for post_id in created_ids:
        try:
            db_client.delete_post_by_id(post_id)
        except Exception as e:
            print(f"Не удалось удалить пост с ID {post_id}: {e}")
