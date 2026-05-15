"""ТК2. Авторизация без токена"""

import allure
import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("Yandex Disk")
@allure.feature("Авторизация")
@allure.story("Попытка авторизации без токена")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.yandex
@pytest.mark.negative
@pytest.mark.d3
def test_yandex_auth_without_token(
    yandex_disk_api_client: YandexDiskApiClient,
) -> None:
    with allure.step(
        "Отправляем запрос на получение информации о пользователе без токена"
    ):
        response = yandex_disk_api_client.get_disk_info_unauthorized()

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step(f"Проверяем статус код ответа"):
        assert (
            parsed.status_code == 401
        ), f"Ожидался статус 401 UNAUTHORIZED, но получен {parsed.status_code}"

    with allure.step(f"Проверяем есть ли поле ошибки в ответе"):
        assert (
            parsed.body["error"]
            and parsed.body["description"]
            and parsed.body["message"]
        ), f"Тело ответа не содержит поля ошибки: {parsed.body}"
