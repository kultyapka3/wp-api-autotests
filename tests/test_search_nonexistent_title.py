"""ТК010. Поиск поста по несуществующему заголовку"""

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
@pytest.mark.d2
def test_search_nonexistent_title(
    api_client: WordPressApiClient,
    db_client: WordPressDbClient,
) -> None:
    search = "123NONEXISTENT_TITLE321"

    response = api_client.get_posts_list(search=search)
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 200
    ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    assert (
        isinstance(parsed.body, list) and len(parsed.body) == 0
    ), f"Ответ не является пустым списком: {parsed.body}"
