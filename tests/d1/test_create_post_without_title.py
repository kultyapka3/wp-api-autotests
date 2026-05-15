"""ТК004. Создание поста без title"""

import allure
import pytest

from clients.wp_api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("WordPress DB")
@allure.feature("Управление постами")
@allure.story("Создание поста без title")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
@pytest.mark.d1
def test_create_post_without_title(
    wp_api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    cleanup_posts: list[int],
) -> None:
    with allure.step("Создание поста без title"):
        response = wp_api_client.create_post(status="draft", content="No Title")

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статуса ответа"):
        assert (
            parsed.status_code == 201
        ), f"Ожидался статус 201 Created, но получен {parsed.status_code}"

    post_id: int = parsed.body["id"]
    cleanup_posts.append(post_id)

    with allure.step("Проверка тела ответа"):
        assert (
            parsed.body["title"]["rendered"] == ""
            and parsed.body["status"] == "draft"
            and parsed.body["content"]["raw"] == "No Title"
        ), "Тело ответа не содержит переданных параметров"

    result = db_client.get_post_by_id(post_id)

    with allure.step("Проверка данных в БД"):
        assert (
            result is not None and result["post_title"] == ""
        ), f"Пост с ID {post_id} не был создан или имеет неверные данные"
