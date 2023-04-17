from dataclasses import dataclass
from typing import Optional, List

from src.client.client import HttpClient
from config import base_url


@dataclass
class Category:
    pk: int
    name: str
    slug: str
    url: str


def get_categories() -> Optional[List[Category]]:
    headers = {
        "accept": "application/json"
    }
    url = base_url + "/api/v1/category-list/"
    client = HttpClient(
        url=url,
        headers=headers
    )
    response = client.http_get()
    if not response:
        return None
    data = client.decode_json(response)
    if not data:
        return None
    categories: List[Category] = []
    for c in data:
        categories.append(Category(
            pk=c.get("id"),
            url=c.get("url"),
            name=c.get("name"),
            slug=c.get("slug")
        ))
    return categories
