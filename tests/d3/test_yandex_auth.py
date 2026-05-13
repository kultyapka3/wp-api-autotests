"""ТК1. Авторизация с валидным токеном"""

import allure
import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("Yandex Disk")
@allure.feature("Авторизация")
@allure.story("Получение информации о пользователе")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.yandex
@pytest.mark.positive
@pytest.mark.d3
def test_yandex_auth(
    yandex_disk_api_client: YandexDiskApiClient,
) -> None:
    with allure.step("Получение информации о пользователе"):
        response = yandex_disk_api_client.get_disk_info()

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статуса ответа"):
        assert (
            parsed.status_code == 200
        ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    with allure.step(
        "Проверка наличия поля user, в котором содержатся login и display_name"
    ):
        assert (
            parsed.body["user"]
            and "login" in parsed.body["user"]
            and "display_name" in parsed.body["user"]
        ), f"Тело ответа не содержит поле user: {parsed.body}"
