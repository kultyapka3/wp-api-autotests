"""ТК013. Восстановление папки"""

import allure
import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("Yandex Disk")
@allure.feature("Управление папками")
@allure.story("Восстановление папки")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.yandex
@pytest.mark.positive
@pytest.mark.d4
def test_restore_folder(
    yandex_disk_api_client: YandexDiskApiClient, test_trash_folder: str
) -> None:
    with allure.step("Восстановление папки"):
        response = yandex_disk_api_client.restore_folder(test_trash_folder)

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статус-кода"):
        assert (
            parsed.status_code == 201
        ), f"Ожидался статус 201 Created, но получен {parsed.status_code}"

    with allure.step("Проверка поля href"):
        assert (
            parsed.body["href"] and "TestFolder" in parsed.body["href"]
        ), f"Тело ответа не содержит поле href с переданным параметром: {parsed.body}"
