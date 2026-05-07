"""Клиент для работы с Yandex Disk API"""

from typing import Final

import requests

from clients.base_api_client import BaseApiClient
from config import YANDEX_DISK_API_URL, YANDEX_DISK_TOKEN

ENDPOINT_DISK_INFO: Final[str] = "/v1/disk"


class YandexDiskApiClient(BaseApiClient):
    """Класс для работы с Yandex Disk API"""

    def __init__(self) -> None:
        super().__init__(
            base_url=YANDEX_DISK_API_URL,
            headers={"Authorization": f"OAuth {YANDEX_DISK_TOKEN}"},
        )

    def get_disk_info(self) -> requests.Response:
        """Получает информацию о диске"""
        return self.get(ENDPOINT_DISK_INFO)

    def get_disk_info_unauthorized(self) -> requests.Response:
        """Пытается получить информацию о диске без токена"""
        return requests.get(f"{YANDEX_DISK_API_URL}{ENDPOINT_DISK_INFO}")
