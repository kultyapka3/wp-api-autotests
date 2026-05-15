"""ТК005. Обновление несуществующего поста"""

import allure
import pytest

from clients.wp_api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("WordPress DB")
@allure.feature("Управление постами")
@allure.story("Обновление несуществующего поста")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
@pytest.mark.d1
def test_update_nonexistent_post(
    wp_api_client: WordPressApiClient,
    db_client: WordPressDbClient,
) -> None:
    nonexistent_post_id: int = 9999

    with allure.step("Обновление поста"):
        response = wp_api_client.update_post(
            post_id=nonexistent_post_id, title="New Title"
        )

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статус-кода"):
        assert (
            parsed.status_code == 404
        ), f"Ожидался статус 404 Not Found, но получен {parsed.status_code}"

    with allure.step("Проверка наличия ошибки в ответе"):
        assert (
            "error" in parsed.body or "message" in parsed.body
        ), 'В ответе отсутствует "error" или "message"'

    result = db_client.get_count_posts_by_id(nonexistent_post_id)

    with allure.step("Проверка отсутствия поста в БД"):
        assert result == 0, f"Существует пост с ID = {nonexistent_post_id}"
