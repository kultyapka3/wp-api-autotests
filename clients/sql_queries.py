"""SQL-запросы"""

from typing import Final

SELECT_POST_BY_ID: Final[str] = (
    "SELECT post_title, post_content FROM wp_posts WHERE ID = %s"
)
DELETE_POST_AND_REVISION: Final[str] = (
    "DELETE FROM wp_posts WHERE ID = %s OR post_parent = %s"
)
SELECT_COUNT_POSTS_BY_ID: Final[str] = (
    "SELECT COUNT(*) as cnt FROM wp_posts WHERE ID = %s"
)
CREATE_TEST_POST: Final[str] = """
    INSERT INTO wp_posts 
    (post_title, post_content, post_status, post_date, post_modified, post_date_gmt, post_modified_gmt, 
    post_excerpt, to_ping, pinged, post_content_filtered) 
    VALUES (%s, %s, %s, NOW(), NOW(), NOW(), NOW(), '', '', '', '')
"""
