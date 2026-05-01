from config import WP_API_URL, WP_API_USER, WP_API_PASS
import requests

class WordPressApiClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.auth = (WP_API_USER, WP_API_PASS)
        self.base_url = f'{WP_API_URL}/index.php?rest_route=/wp/v2'

    def create_post(self, title: str, status: str = 'draft', content: str = '') -> requests.Response:
        payload = {'title': title, 'status': status, 'content': content}

        return self.session.post(f'{self.base_url}/posts', json=payload)

    def update_post(self, post_id: int, title: str, content: str = '') -> requests.Response:
        payload = {'title': title, 'content': content}

        return self.session.post(f'{self.base_url}/posts/{post_id}', json=payload)

    def delete_post(self, post_id: int, force: bool = True) -> requests.Response:
        return self.session.delete(
            f'{self.base_url}/posts/{post_id}', params={'force': force}
        )
