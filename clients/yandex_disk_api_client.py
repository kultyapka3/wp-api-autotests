"""Клиент для работы с Yandex Disk API"""

from typing import Final

import requests

from clients.base_api_client import BaseApiClient
from config import YANDEX_DISK_API_URL, YANDEX_DISK_TOKEN

ENDPOINT_DISK_INFO: Final[str] = "/v1/disk"
ENDPOINT_RESOURCES: Final[str] = "/v1/disk/resources"
ENDPOINT_TRASH_RESOURCES: Final[str] = "/v1/disk/trash/resources"
ENDPOINT_TRASH_RESTORE: Final[str] = "/v1/disk/trash/resources/restore"


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

    def create_folder(self, path: str) -> requests.Response:
        """Создает папку"""
        return self.put(ENDPOINT_RESOURCES, params={"path": path})

    def delete_folder(self, path: str, permanently: bool = False) -> requests.Response:
        """Удаляет или перемещает папку в корзину"""
        params = {"path": path}

        if permanently:
            params["permanently"] = "true"

        return self.delete(ENDPOINT_RESOURCES, params=params)

    def get_trash_resources(self) -> requests.Response:
        """Возвращает список ресурсов в корзине в виде ответа"""
        return self.get(ENDPOINT_TRASH_RESOURCES)

    def restore_folder(self, trash_path: str) -> requests.Response:
        """Восстанавливает папку из корзины"""
        return self.put(ENDPOINT_TRASH_RESTORE, params={"path": trash_path})
