"""ТК014. Создание уже существующей папки"""

import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.yandex
@pytest.mark.negative
@pytest.mark.d4
def test_create_existing_folder(
    yandex_disk_api_client: YandexDiskApiClient, test_folder: str
) -> None:
    response = yandex_disk_api_client.create_folder(test_folder)
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 409
    ), f"Ожидался статус 409 Conflict, но получен {parsed.status_code}"

    assert (
        parsed.body["error"] and parsed.body["message"]
    ), f"Тело ответа не содержит поля ошибки: {parsed.body}"
