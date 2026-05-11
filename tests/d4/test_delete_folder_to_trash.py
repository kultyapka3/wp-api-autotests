"""ТК012. Удаление папки (перемещение в корзину)"""

import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.yandex
@pytest.mark.positive
@pytest.mark.d4
def test_delete_folder_to_trash(
    yandex_disk_api_client: YandexDiskApiClient, test_folder: str
) -> None:
    response = yandex_disk_api_client.delete_folder(test_folder)
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 204
    ), f"Ожидался статус 204 No Content, но получен {parsed.status_code}"

    assert not parsed.body, f"Тело ответа должно быть пустым: {parsed.body}"
