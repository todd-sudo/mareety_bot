from typing import Optional

from aiogram.utils.markdown import hlink, hbold

from src.client.client import HttpClient
from config import base_url


def get_product_list_by_category_id(
        category_id: int, page: str
) -> Optional[dict]:
    headers = {
        "accept": "application/json"
    }
    url = base_url + f"/api/v1/product-list/{category_id}/{page}"
    client = HttpClient(url=url, headers=headers)
    response = client.http_get()
    if not response or response.status_code != 200:
        return None
    data = client.decode_json(response)
    return data


def parse_product(item: dict) -> tuple[str, str]:
    cur = "UZS"
    title = item.get("title")
    url = item.get("url")
    category = item.get("category").get("name")
    slug = item.get("slug")
    image = item.get("image")
    description = item.get("description")
    price = item.get("price")
    image = hlink("🖥", image)

    msg = """
{0} {1}

{2}
{3} {4}
{5}


""".format(image, category, hlink(title, url), price, cur, description)
    return msg, slug


