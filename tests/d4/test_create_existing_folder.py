"""ТК014. Создание уже существующей папки"""

import allure
import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("Yandex Disk")
@allure.feature("Управление папками")
@allure.story("Создание уже существующей папки")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.yandex
@pytest.mark.negative
@pytest.mark.d4
def test_create_existing_folder(
    yandex_disk_api_client: YandexDiskApiClient, test_folder: str
) -> None:
    with allure.step("Создаем папку с уже существующим именем"):
        response = yandex_disk_api_client.create_folder(test_folder)

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверяем статус код ответа"):
        assert (
            parsed.status_code == 409
        ), f"Ожидался статус 409 Conflict, но получен {parsed.status_code}"

    with allure.step("Проверяем есть ли ошибка в теле ответа"):
        assert (
            parsed.body["error"] and parsed.body["message"]
        ), f"Тело ответа не содержит поля ошибки: {parsed.body}"
