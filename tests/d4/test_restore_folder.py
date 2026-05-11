"""ТК013. Восстановление папки"""

import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.yandex
@pytest.mark.positive
@pytest.mark.d4
def test_restore_folder(
    yandex_disk_api_client: YandexDiskApiClient, test_trash_folder: str
) -> None:
    response = yandex_disk_api_client.restore_folder(test_trash_folder)
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 201
    ), f"Ожидался статус 201 Created, но получен {parsed.status_code}"

    assert (
        parsed.body["href"] and "TestFolder" in parsed.body["href"]
    ), f"Тело ответа не содержит поле href с переданным параметром: {parsed.body}"
