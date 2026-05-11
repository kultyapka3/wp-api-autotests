"""ТК011. Создание папки"""

import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.yandex
@pytest.mark.positive
@pytest.mark.d4
def test_create_folder(
    yandex_disk_api_client: YandexDiskApiClient, cleanup_test_folders: list[str]
) -> None:
    folder_name = "FolderForTest"
    response = yandex_disk_api_client.create_folder(folder_name)
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 201
    ), f"Ожидался статус 201 Created, но получен {parsed.status_code}"

    cleanup_test_folders.append(folder_name)

    assert (
        parsed.body["href"] and folder_name in parsed.body["href"]
    ), f"Тело ответа не содержит поле href с переданным параметром: {parsed.body}"
