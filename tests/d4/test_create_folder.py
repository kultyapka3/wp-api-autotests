"""ТК011. Создание папки"""

import allure
import pytest

from clients.yandex_disk_api_client import YandexDiskApiClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("Yandex Disk")
@allure.feature("Управление папками")
@allure.story("Создание папки")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.yandex
@pytest.mark.positive
@pytest.mark.d4
def test_create_folder(
    yandex_disk_api_client: YandexDiskApiClient, cleanup_folders: list[str]
) -> None:
    folder_name = "FolderForTest"

    with allure.step(f"Создаем папку с именем {folder_name}"):
        response = yandex_disk_api_client.create_folder(folder_name)

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверяем, что статус ответа равен 201 Created"):
        assert (
            parsed.status_code == 201
        ), f"Ожидался статус 201 Created, но получен {parsed.status_code}"

    cleanup_folders.append(folder_name)

    with allure.step(
        "Проверяем, что в теле ответа содержится поле href с именем папки"
    ):
        assert (
            parsed.body["href"] and folder_name in parsed.body["href"]
        ), f"Тело ответа не содержит поле href с переданным параметром: {parsed.body}"
