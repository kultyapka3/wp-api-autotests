"""Парсер ответов API"""

from dataclasses import dataclass

import requests


@dataclass
class ParsedResponse:
    """Структурированный ответ"""

    status_code: int
    body: dict


def parse_api_response(response: requests.Response) -> ParsedResponse:
    """Извлекает статус и тело"""
    status_code = response.status_code

    try:
        body = response.json()
    except requests.JSONDecodeError:
        body = {}

    return ParsedResponse(status_code=status_code, body=body)
