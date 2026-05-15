"""ТК003. Удаление поста"""

import allure
import pytest

from clients.wp_api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@allure.epic("WordPress DB")
@allure.feature("Управление постами")
@allure.story("Удаление поста")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
@pytest.mark.d1
def test_delete_post(
    wp_api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    new_post: int,
) -> None:
    with allure.step("Удаление поста"):
        response = wp_api_client.delete_post(post_id=new_post, force=True)

    parsed: ParsedResponse = parse_api_response(response)

    with allure.step("Проверка статуса ответа"):
        assert (
            parsed.status_code == 200
        ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    result = db_client.get_count_posts_by_id(new_post)

    with allure.step("Проверка, что пост был удален"):
        assert result == 0, f"Пост с ID = {new_post} не был удален"
