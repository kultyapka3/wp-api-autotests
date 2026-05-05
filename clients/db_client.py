"""DB клиент"""

import mysql.connector

from clients.sql_queries import (
    SELECT_POST_BY_ID,
    DELETE_POST_AND_REVISION,
    CREATE_TEST_POST,
    SELECT_COUNT_POSTS_BY_ID,
)
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


class WordPressDbClient:
    """Клиент для работы с БД WordPress"""

    def __init__(self) -> None:
        self._config = {
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME,
            "user": DB_USER,
            "password": DB_PASS,
        }

    def _get_connection(self) -> mysql.connector.connection.MySQLConnection:
        return mysql.connector.connect(**self._config)

    def _execute_query(self, query: str, params: tuple = None) -> list:
        """Внутренний SELECT запрос"""
        with self._get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)

                return cursor.fetchall()

    def _execute_update(self, query: str, params: tuple = None) -> int:
        """Внутренний INSERT/UPDATE/DELETE запрос"""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()

                return cursor.rowcount

    def get_post_by_id(self, post_id: int) -> dict | None:
        """Получает пост по ID"""
        results = self._execute_query(SELECT_POST_BY_ID, (post_id,))

        return results[0] if results else None

    def get_count_posts_by_id(self, post_id: int) -> int:
        """Получает количество постов по ID"""
        results = self._execute_query(SELECT_COUNT_POSTS_BY_ID, (post_id,))

        return results[0]["cnt"]

    def delete_post_by_id(self, post_id: int) -> None:
        """Удаляет пост и его ревизию по ID"""
        self._execute_update(DELETE_POST_AND_REVISION, (post_id, post_id))

    def create_test_post(
        self, title: str, content: str, status: str = "publish"
    ) -> int:
        """Создает тестовый пост напрямую"""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(CREATE_TEST_POST, (content, title, status))
                conn.commit()

                return cursor.lastrowid
