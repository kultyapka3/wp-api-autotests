"""ТК009. Получение несуществующего поста"""

import allure
import pytest

from clients.wp_api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("WordPress DB")
@allure.feature("Получение данных")
@allure.story("Получение несуществующего поста")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
@pytest.mark.d2
def test_get_nonexistent_post(
    wp_api_client: WordPressApiClient,
    db_client: WordPressDbClient,
) -> None:
    nonexistent_id: int = 9999

    with allure.step("Получение поста с несуществующим ID"):
        response = wp_api_client.get_post(nonexistent_id)

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статус-кода"):
        assert (
            parsed.status_code == 404
        ), f"Ожидался статус 404 Not Found, но получен {parsed.status_code}"

    with allure.step("Проверка наличия сообщения об ошибке"):
        assert (
            "error" in parsed.body or "message" in parsed.body
        ), "В ответе отсутствует поле 'error' или 'message'"
