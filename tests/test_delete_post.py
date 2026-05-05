"""ТК003. Удаление поста"""

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
def test_delete_post(
    api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    test_post: int,
    cleanup_test_posts: list,
) -> None:
    response = api_client.delete_post(post_id=test_post, force=True)
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 200
    ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    result = db_client.get_count_posts_by_id(test_post)

    assert result == 0, f"Пост с ID = {test_post} не был удален"
