from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
import pytest

@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
def test_update_nonexistent_post(api_client: WordPressApiClient, db_client: WordPressDbClient) -> None:
    response = api_client.session.post(
        f'{api_client.base_url}/posts/9999',
        json={'title': 'New Title'}
    )

    status_code: int = response.status_code

    assert status_code == 404, \
        f'Ожидался статус 404 Not Found, но получен {status_code}'
    assert 'error' in response.json() or 'message' in response.json(), \
        'В ответе отсутствует "error" или "message"'

    result = db_client.execute_query(
        'SELECT COUNT(*) as cnt FROM wp_posts WHERE ID = 9999'
    )

    assert result[0]['cnt'] == 0, \
        'Существует пост с ID = 9999'
