"""ТК007. Получение существующего поста по ID"""

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
@pytest.mark.d2
def test_get_post_by_id(
    api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    test_post: int
) -> None:
    response = api_client.get_post(post_id=test_post)
    parsed: ParsedResponse = parse_api_response(response)
    post_id: int = parsed.body["id"]

    assert (
        parsed.status_code == 200
    ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"
    assert (
        parsed.body["id"] == post_id
    ), f"ID в ответе ({parsed.body["id"]}) не совпадает с созданным ({post_id})"

    result = db_client.get_post_by_id(post_id)

    assert (
        result is not None and result["post_title"] == "Test Title"
    ), f"Пост с ID {post_id} не найден в БД или имеет неверные данные"
