from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
import pytest
from typing import Iterator

@pytest.fixture()
def api_client() -> WordPressApiClient:
    return WordPressApiClient()

@pytest.fixture()
def db_client() -> WordPressDbClient:
    return WordPressDbClient()

@pytest.fixture()
def test_post(db_client: WordPressDbClient) -> Iterator[int]:
    """Создание тестового поста"""
    post_id = db_client.create_test_post(
        title='Test Title',
        content='Test Content'
    )
    yield post_id

@pytest.fixture(autouse=True)
def cleanup_test_posts(db_client: WordPressDbClient):
    """Удаление созданных в тесте постов"""
    created_ids: list[int] = []
    yield created_ids

    for post_id in created_ids:
        try:
            db_client.delete_post_by_id(post_id)
        except Exception as e:
            print(f'Не удалось удалить пост с ID {post_id}: {e}')
