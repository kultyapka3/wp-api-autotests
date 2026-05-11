"""Фикстуры для тестов"""

from typing import Iterator, Callable

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import parse_api_response, ParsedResponse


@pytest.fixture()
def api_client() -> WordPressApiClient:
    """Фикстура для API клиента"""
    return WordPressApiClient()


@pytest.fixture()
def db_client() -> WordPressDbClient:
    """Фикстура для БД клиента"""
    return WordPressDbClient()


@pytest.fixture()
def yandex_disk_api_client() -> YandexDiskApiClient:
    """Фикстура для API клиента Yandex Disk"""
    return YandexDiskApiClient()


@pytest.fixture()
def test_post(db_client: WordPressDbClient) -> Iterator[int]:
    """Создание тестового поста"""
    post_id = db_client.create_test_post(title="Test Title", content="Test Content")
    yield post_id

    try:
        db_client.delete_post_by_id(post_id)
    except Exception:
        pass


@pytest.fixture()
def test_post_factory(db_client: WordPressDbClient) -> Iterator[Callable[[], int]]:
    """Создание тестового поста по вызову"""
    created_ids: list[int] = []

    def _create() -> int:
        post_id = db_client.create_test_post(title="Test Title", content="Test Content")
        created_ids.append(post_id)

        return post_id

    yield _create

    for pid in created_ids:
        try:
            db_client.delete_post_by_id(pid)
        except Exception:
            pass


@pytest.fixture()
def test_folder(yandex_disk_api_client: YandexDiskApiClient) -> Iterator[str]:
    """Создание тестовой папки"""
    folder_name = "TestFolder"
    yandex_disk_api_client.create_folder(folder_name)
    yield folder_name

    response = yandex_disk_api_client.delete_folder(folder_name, True)

    if response.status_code == 404:
        try:
            response = yandex_disk_api_client.get_trash_resources()
            parsed: ParsedResponse = parse_api_response(response)
            items = parsed.body.get("_embedded", {}).get("items", [])
            target_folder_path = next(
                (item for item in items if item.get("name") == folder_name), None
            )

            yandex_disk_api_client.restore_folder(target_folder_path["path"])
            yandex_disk_api_client.delete_folder(folder_name, True)
        except Exception:
            pass


@pytest.fixture()
def test_trash_folder(yandex_disk_api_client: YandexDiskApiClient) -> Iterator[str]:
    """Создание тестовой папки в корзине"""
    folder_name = "TestFolder"
    yandex_disk_api_client.create_folder(folder_name)
    yandex_disk_api_client.delete_folder(folder_name)

    response = yandex_disk_api_client.get_trash_resources()
    parsed: ParsedResponse = parse_api_response(response)
    items = parsed.body.get("_embedded", {}).get("items", [])
    target_folder_path = next(
        (item for item in items if item.get("name") == folder_name), None
    )
    yield target_folder_path["path"]

    response = yandex_disk_api_client.delete_folder(folder_name, True)

    if response.status_code == 404:
        try:
            yandex_disk_api_client.restore_folder(target_folder_path["path"])
            yandex_disk_api_client.delete_folder(folder_name, True)
        except Exception:
            pass


@pytest.fixture(autouse=True)
def cleanup_test_posts(db_client: WordPressDbClient) -> Iterator[list[int]]:
    """Удаление созданных в тесте постов"""
    created_ids: list[int] = []
    yield created_ids

    for post_id in created_ids:
        try:
            db_client.delete_post_by_id(post_id)
        except Exception:
            pass


@pytest.fixture(autouse=True)
def cleanup_test_folders(
    yandex_disk_api_client: YandexDiskApiClient,
) -> Iterator[list[str]]:
    """Удаление созданных в тесте папок"""
    created_names: list[str] = []
    yield created_names

    for folder_name in created_names:
        try:
            yandex_disk_api_client.delete_folder(folder_name, True)
        except Exception:
            pass
