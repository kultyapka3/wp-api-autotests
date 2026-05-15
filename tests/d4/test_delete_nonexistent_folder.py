"""ТК015. Удаление несуществующей папки"""

import allure
import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("Yandex Disk")
@allure.feature("Управление папками")
@allure.story("Удаление несуществующей папки")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.yandex
@pytest.mark.negative
@pytest.mark.d4
def test_delete_nonexistent_folder(yandex_disk_api_client: YandexDiskApiClient) -> None:
    nonexistent_folder_name = "123NONEXISTENT_FOLDER321"

    with allure.step(
        f"Удаляем несуществующую папку с именем {nonexistent_folder_name}"
    ):
        response = yandex_disk_api_client.delete_folder(nonexistent_folder_name)

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверяем, что статус ответа равен 404 Not Found"):
        assert (
            parsed.status_code == 404
        ), f"Ожидался статус 404 Not Found, но получен {parsed.status_code}"

    with allure.step("Проверяем, что в теле ответа есть ошибка и сообщение об ошибке"):
        assert (
            parsed.body["error"] and parsed.body["message"]
        ), f"Тело ответа не содержит поля ошибки: {parsed.body}"
