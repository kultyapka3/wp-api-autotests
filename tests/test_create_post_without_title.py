"""ТК004. Создание поста без title"""

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
@pytest.mark.d1
def test_create_post_without_title(
    api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    cleanup_test_posts: list[int],
) -> None:
    response = api_client.create_post(status="draft", content="No Title")
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 201
    ), f"Ожидался статус 201 Created, но получен {parsed.status_code}"

    post_id: int = parsed.body["id"]
    cleanup_test_posts.append(post_id)

    assert (
        parsed.body["title"]["rendered"] == ""
        and parsed.body["status"] == "draft"
        and parsed.body["content"]["raw"] == "No Title"
    ), "Тело ответа не содержит переданных параметров"

    result = db_client.get_post_by_id(post_id)

    assert (
        result is not None and result["post_title"] == ""
    ), f"Пост с ID {post_id} не был создан или имеет неверные данные"
