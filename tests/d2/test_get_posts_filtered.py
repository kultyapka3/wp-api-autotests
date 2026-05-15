"""ТК008. Получение списка постов с фильтрацией по статусу"""

from typing import Callable

import allure
import pytest

from clients.wp_api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("WordPress DB")
@allure.feature("Получение данных")
@allure.story("Получение списка постов с фильтрацией по статусу")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
@pytest.mark.d2
def test_get_posts_filtered(
    wp_api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    new_post_factory: Callable[[], int],
) -> None:
    ids = [new_post_factory(), new_post_factory()]

    with allure.step("Получение списка постов с фильтрацией по статусу"):
        response = wp_api_client.get_posts_list(status="publish")

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статуса ответа"):
        assert (
            parsed.status_code == 200
        ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    response_ids = [p["id"] for p in parsed.body if "id" in p]

    with allure.step("Проверка соответствия ID в ответе и созданных"):
        assert (
            ids[0] in response_ids and ids[-1] in response_ids
        ), f"ID в ответе ({response_ids}) не совпадают с созданным ({ids})"

    statuses = {p["status"] for p in parsed.body if "status" in p and "id" in p}

    with allure.step("Проверка соответствия статусов в ответе и ожидаемых"):
        assert statuses == {
            "publish"
        }, f"Статусы в ответе не являются ожидаемыми: {statuses - {'publish'}}"
