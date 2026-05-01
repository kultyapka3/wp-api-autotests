from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
import pytest

@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
def test_delete_post(api_client: WordPressApiClient, db_client: WordPressDbClient, cleanup_test_posts: list) -> None:
    post_id: int = db_client.create_test_post('Test Post 2', 'Test Content 2')
    cleanup_test_posts.append(post_id)

    response = api_client.delete_post(post_id=post_id, force=True)

    status_code: int = response.status_code

    assert status_code == 200, \
        f'Ожидался статус 200 OK, но получен {status_code}'

    result = db_client.execute_query(
        'SELECT COUNT(*) as cnt FROM wp_posts WHERE ID = %s', (post_id,)
    )

    assert result[0]['cnt'] == 0, \
        f'Пост с ID = {post_id} не был удален'
