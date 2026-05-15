"""ТК002. Обновление поста"""

import allure
import pytest

from clients.wp_api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("WordPress DB")
@allure.feature("Управление постами")
@allure.story("Обновление поста")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
@pytest.mark.d1
def test_update_post(
    wp_api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    new_post: int,
) -> None:
    with allure.step("Обновление поста"):
        response = wp_api_client.update_post(
            post_id=new_post, title="Updated Title", content="Updated Content"
        )

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статуса ответа"):
        assert (
            parsed.status_code == 200
        ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    with allure.step("Проверка содержимого ответа"):
        assert (
            parsed.body["title"]["rendered"] == "Updated Title"
            and parsed.body["content"]["raw"] == "Updated Content"
        ), "Тело ответа не содержит переданных параметров"

    result = db_client.get_post_by_id(new_post)

    with allure.step("Проверка обновленного поста в БД"):
        assert (
            result is not None and result["post_title"] == "Updated Title"
        ), f"Пост с ID {new_post} не был обновлен"
