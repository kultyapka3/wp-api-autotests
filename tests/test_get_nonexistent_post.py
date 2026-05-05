"""ТК009. Получение несуществующего поста"""

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
@pytest.mark.d2
def test_get_nonexistent_post(
    api_client: WordPressApiClient,
    db_client: WordPressDbClient,
) -> None:
    nonexistent_id: int = 9999
    response = api_client.get_post(nonexistent_id)
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 404
    ), f"Ожидался статус 404 Not Found, но получен {parsed.status_code}"

    assert (
        "error" in parsed.body or "message" in parsed.body
    ), "В ответе отсутствует поле 'error' или 'message'"
