"""ТК003. Удаление поста"""

from typing import Callable

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
@pytest.mark.d1
def test_delete_post(
    api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    test_post_factory: Callable[[], int],
) -> None:
    post_id = test_post_factory()
    response = api_client.delete_post(post_id=post_id, force=True)
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 200
    ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    result = db_client.get_count_posts_by_id(post_id)

    assert result == 0, f"Пост с ID = {post_id} не был удален"
