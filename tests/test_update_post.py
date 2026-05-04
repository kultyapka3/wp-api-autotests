from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
import pytest
from utils.response_parser import ParsedResponse, parse_api_response

@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
def test_update_post(api_client: WordPressApiClient, db_client: WordPressDbClient, test_post: int, cleanup_test_posts: list) -> None:
    response = api_client.update_post(post_id=test_post, title='Updated Title', content='Updated Content')
    parsed: ParsedResponse = parse_api_response(response)

    post_id: int = parsed.body['id']
    cleanup_test_posts.append(post_id)

    assert parsed.status_code == 200, \
        f'Ожидался статус 200 OK, но получен {parsed.status_code}'
    assert parsed.body['title']['rendered'] == 'Updated Title', \
        'Ожидалось, что тело ответа будет содержать переданные параметры'

    result = db_client.get_post_by_id(post_id)

    assert result is not None and result['post_title'] == 'Updated Title', \
        f'Пост с ID {post_id} не был обновлен'
