from src.client.client import HttpClient
from config import base_url


def create_user(
    tg_user_id: str,
    first_name: str,
    last_name: str,
    phone: str,
    address: str,
    lang: str,
) -> bool:
    headers = {
        "accept": "application/json"
    }
    url = base_url + "/api/v1/create-customer/"
    json_data = {
        "tg_user_id": tg_user_id,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "address": address,
        "lang": lang,
    }
    client = HttpClient(
        url=url,
        headers=headers,
        json_data=json_data
    )
    response = client.http_post_json()
    if response:
        return True
    return False
