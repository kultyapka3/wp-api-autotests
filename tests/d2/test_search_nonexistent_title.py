"""ТК010. Поиск поста по несуществующему заголовку"""

import allure
import pytest

from clients.wp_api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("WordPress DB")
@allure.feature("Получение данных")
@allure.story("Поиск поста по несуществующему заголовку")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
@pytest.mark.d2
def test_search_nonexistent_title(
    wp_api_client: WordPressApiClient,
    db_client: WordPressDbClient,
) -> None:
    search = "123NONEXISTENT_TITLE321"

    with allure.step("Выполняем запрос на получение списка постов"):
        response = wp_api_client.get_posts_list(search=search)

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверяем статус ответа"):
        assert (
            parsed.status_code == 200
        ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    with allure.step("Проверяем тело ответа"):
        assert (
            isinstance(parsed.body, list) and len(parsed.body) == 0
        ), f"Ответ не является пустым списком: {parsed.body}"
