from clients.api_client import WordPressApiClient
from clients.db_client import WordPressDbClient
import pytest

@pytest.mark.wp
@pytest.mark.negative
@pytest.mark.posts
def test_create_post_without_title(api_client: WordPressApiClient, db_client: WordPressDbClient, cleanup_test_posts: list) -> None:
    response = api_client.session.post(
        f'{api_client.base_url}/posts',
        json={'status': 'draft', 'content': 'No Title'}
    )

    post_id: int = response.json()['id']
    cleanup_test_posts.append(post_id)

    status_code: int = response.status_code

    assert status_code == 201, \
        f'Ожидался статус 201 Created, но получен {status_code}'
    assert response.json()['title']['rendered'] == '' and response.json()['status'] == 'draft', \
        'Ожидалось, что тело ответа будет содержать переданные параметры'

    result = db_client.execute_query(
        'SELECT post_title, post_content FROM wp_posts WHERE ID = %s', (post_id,)
    )

    assert result and result[0]['post_title'] == '', \
        f'Пост без заголовка с ID {post_id} не был создан'
