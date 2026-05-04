from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
import pytest
from utils.response_parser import ParsedResponse, parse_api_response

@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
def test_update_nonexistent_post(api_client: WordPressApiClient, db_client: WordPressDbClient) -> None:
    nonexistent_post_id: int = 9999
    response = api_client.update_post(post_id=nonexistent_post_id, title='New Title')
    parsed: ParsedResponse = parse_api_response(response)

    assert parsed.status_code == 404, \
        f'Ожидался статус 404 Not Found, но получен {parsed.status_code}'
    assert 'error' in parsed.body or 'message' in parsed.body, \
        'В ответе отсутствует "error" или "message"'

    result = db_client.get_count_posts_by_id(nonexistent_post_id)

    assert result == 0, \
        f'Существует пост с ID = {nonexistent_post_id}'
