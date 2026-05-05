"""ТК008. Получение списка постов с фильтрацией по статусу"""

from typing import Callable

import pytest

from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
from utils.response_parser import ParsedResponse, parse_api_response


@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
@pytest.mark.d2
def test_get_posts_filtered(
    api_client: WordPressApiClient,
    db_client: WordPressDbClient,
    test_post_factory: Callable[[], int],
    cleanup_test_posts: list[int],
) -> None:
    ids = [test_post_factory(), test_post_factory()]
    cleanup_test_posts.extend(ids)

    response = api_client.get_posts_list(status="publish")
    parsed: ParsedResponse = parse_api_response(response)

    assert (
        parsed.status_code == 200
    ), f"Ожидался статус 200 OK, но получен {parsed.status_code}"

    response_ids = [p["id"] for p in parsed.body if "id" in p]

    assert (
        ids[0] in response_ids and ids[-1] in response_ids
    ), f"ID в ответе ({response_ids}) не совпадают с созданным ({ids})"

    statuses = {p["status"] for p in parsed.body if "status" in p and "id" in p}

    assert (
        statuses == {"publish"}
    ), f"Статусы в ответе не являются ожидаемыми: {statuses - {'publish'}}"
