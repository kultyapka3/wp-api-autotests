"""ТК012. Удаление папки (перемещение в корзину)"""

import allure
import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("Yandex Disk")
@allure.feature("Управление папками")
@allure.story("Удаление папки (перемещение в корзину)")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.yandex
@pytest.mark.positive
@pytest.mark.d4
def test_delete_folder_to_trash(
    yandex_disk_api_client: YandexDiskApiClient, new_folder: str
) -> None:
    with allure.step("Удаление папки (перемещение в корзину)"):
        response = yandex_disk_api_client.delete_folder(new_folder)

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статуса ответа"):
        assert (
            parsed.status_code == 204
        ), f"Ожидался статус 204 No Content, но получен {parsed.status_code}"

    with allure.step("Проверка тела ответа"):
        assert not parsed.body, f"Тело ответа должно быть пустым: {parsed.body}"
