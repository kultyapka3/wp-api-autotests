"""ТК002. Обновление поста"""

from typing import Callable

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
@pytest.mark.d1
def test_update_post(
    api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    test_post: int
) -> None:
    response = api_client.update_post(
        post_id=test_post, title="Updated Title", content="Updated Content"
    )
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 200
    ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"
    assert (
        parsed.body["title"]["rendered"] == "Updated Title"
        and parsed.body["content"]["raw"] == "Updated Content"
    ), "Тело ответа не содержит переданных параметров"

    result = db_client.get_post_by_id(test_post)

    assert (
        result is not None and result["post_title"] == "Updated Title"
    ), f"Пост с ID {test_post} не был обновлен"
