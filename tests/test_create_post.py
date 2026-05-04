from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
import pytest
from utils.response_parser import ParsedResponse, parse_api_response

@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
def test_create_post(api_client: WordPressApiClient, db_client: WordPressDbClient, cleanup_test_posts: list) -> None:
    response = api_client.create_post(title='TestPost1', status='draft', content='Test content')
    parsed: ParsedResponse = parse_api_response(response)

    assert parsed.status_code == 201, \
        f'Ожидался статус 201 Created, но получен {parsed.status_code}'

    post_id: int = parsed.body['id']
    cleanup_test_posts.append(post_id)

    assert parsed.body['title']['rendered'] == 'TestPost1' and parsed.body['status'] == 'draft', \
        'Тело ответа не содержит переданных параметров'

    result = db_client.get_post_by_id(post_id)

    assert result is not None and result['post_title'] == 'TestPost1', \
        f'Пост с ID {post_id} не был создан или имеет неверные данные'
