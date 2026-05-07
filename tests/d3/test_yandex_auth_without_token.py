"""ТК2. Авторизация без токена"""

import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.yandex
@pytest.mark.negative
@pytest.mark.d3
def test_yandex_auth_without_token(
    yandex_disk_api_client: YandexDiskApiClient,
) -> None:
    response = yandex_disk_api_client.get_disk_info_unauthorized()
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 401
    ), f"Ожидался статус 401 UNAUTHORIZED, но получен {parsed.status_code}"

    assert (
        parsed.body["error"] and parsed.body["description"] and parsed.body["message"]
    ), f"Тело ответа не содержит поле user: {parsed.body}"
