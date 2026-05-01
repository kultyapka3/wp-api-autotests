from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
import pytest

@pytest.mark.wp
@pytest.mark.positive
@pytest.mark.posts
def test_update_post(api_client: WordPressApiClient, db_client: WordPressDbClient, cleanup_test_posts: list) -> None:
    post_id: int = db_client.create_test_post('Original Title', 'Original Content')
    cleanup_test_posts.append(post_id)

    response = api_client.update_post(
        post_id=post_id, title='Updated Title', content='Updated Content'
    )

    status_code: int = response.status_code

    assert status_code == 200, \
        f'Ожидался статус 200 OK, но получен {status_code}'
    assert response.json()['title']['rendered'] == 'Updated Title', \
        'Ожидалось, что тело ответа будет содержать переданные параметры'

    result = db_client.execute_query(
        'SELECT post_title, post_content FROM wp_posts WHERE ID = %s', (post_id,)
    )

    assert result and result[0]['post_title'] == 'Updated Title', \
        f'Пост с ID {post_id} не был обновлен'
