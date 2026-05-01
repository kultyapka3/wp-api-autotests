from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
import pytest

@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
def test_create_post(api_client: WordPressApiClient, db_client: WordPressDbClient, cleanup_test_posts: list) -> None:
    response = api_client.create_post(
        title='TestPost1', status='draft', content='Test content'
    )

    post_id: int = response.json()['id']
    cleanup_test_posts.append(post_id)

    status_code: int = response.status_code

    assert status_code == 201, \
        f'Ожидался статус 201 Created, но получен {status_code}'
    assert response.json()['title']['rendered'] == 'TestPost1' and response.json()['status'] == 'draft', \
        'Ожидалось, что тело ответа будет содержать переданные параметры'

    result = db_client.execute_query(
        'SELECT post_title, post_content FROM wp_posts WHERE ID = %s', (post_id,)
    )

    assert result and result[0]['post_title'] == 'TestPost1', \
        f'Пост с ID {post_id} не был создан'
