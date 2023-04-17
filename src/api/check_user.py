from src.client.client import HttpClient
from config import base_url


def check_user(tg_user_id: str) -> str:
    headers = {
        "accept": "application/json"
    }
    url = base_url + "/api/v1/get-customer/"
    json_data = {
        "tg_user_id": tg_user_id
    }
    client = HttpClient(
        url=url,
        headers=headers,
        json_data=json_data
    )
    response = client.http_post_json()
    print(response)
    if response:
        data = response.json()
        lang = data.get("lang")
        return lang
    return ""
