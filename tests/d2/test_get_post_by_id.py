"""ТК007. Получение существующего поста по ID"""

import allure
import pytest

from clients.wp_api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("WordPress DB")
@allure.feature("Получение данных")
@allure.story("Получение существующего поста по ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
@pytest.mark.d2
def test_get_post_by_id(
    wp_api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    new_post: int,
) -> None:
    with allure.step("Получение поста по ID"):
        response = wp_api_client.get_post(post_id=new_post)

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статус-кода и наличия ID в ответе"):
        assert (
            parsed.status_code == 200
        ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    with allure.step("Проверка ID в ответе"):
        assert (
            parsed.body["id"] == new_post
        ), f"ID в ответе ({parsed.body["id"]}) не совпадает с созданным ({new_post})"

    result = db_client.get_post_by_id(new_post)

    with allure.step("Проверка наличия поста в БД"):
        assert (
            result is not None and result["post_title"] == "Test Title"
        ), f"Пост с ID {new_post} не найден в БД или имеет неверные данные"
