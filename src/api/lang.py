from config import base_url
from src.client.client import HttpClient


def get_customer_lang(tg_user_id: str) -> str:
    headers = {
        "accept": "application/json",
        "tguserid": tg_user_id
    }
    url = base_url + "/api/v1/lang/"
    client = HttpClient(
        url=url,
        headers=headers,
    )
    response = client.http_get()

    if not response or response.status_code != 200:
        return "en"
    data = response.json()
    lang = data.get("lang")
    return lang


def change_customer_lang(tg_user_id: str, lang: str) -> int:
    headers = {
        "accept": "application/json",
        "tguserid": tg_user_id
    }
    json_data = {
        "lang": lang
    }
    url = base_url + "/api/v1/change-lang/"
    client = HttpClient(
        url=url,
        headers=headers,
        json_data=json_data
    )
    response = client.http_post_json()

    if not response or response.status_code != 200:
        return 0
    return response.status_code
