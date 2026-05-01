from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
import mysql.connector

class WordPressDbClient:
    def __init__(self) -> None:
        self.db_config = {
            'host': DB_HOST,
            'port': DB_PORT,
            'database': DB_NAME,
            'user': DB_USER,
            'password': DB_PASS,
        }

    def _get_connection(self) -> mysql.connector.connection.MySQLConnection:
        return mysql.connector.connect(**self.db_config)

    def execute_query(self, query: str, params: tuple = None) -> list:
        """SELECT запрос"""
        with self._get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)

                return cursor.fetchall()

    def execute_update(self, query: str, params: tuple = None) -> int:
        """INSERT/UPDATE/DELETE запрос"""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()

                return cursor.rowcount

    def delete_post_by_id(self, post_id: int) -> None:
        """Удаляет пост и его ревизию по ID"""
        query = 'DELETE FROM wp_posts WHERE ID = %s OR post_parent = %s'
        self.execute_update(query, (post_id, post_id))

    def create_test_post(self, title: str, content: str, status: str = 'publish') -> int:
        """Создает тестовый пост напрямую"""
        query = """
            INSERT INTO wp_posts 
            (post_title, post_content, post_status, post_date, post_modified, post_date_gmt, post_modified_gmt, 
            post_excerpt, to_ping, pinged, post_content_filtered) 
            VALUES (%s, %s, %s, NOW(), NOW(), NOW(), NOW(), '', '', '', '')
        """

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (content, title, status))
                conn.commit()

                return cursor.lastrowid
