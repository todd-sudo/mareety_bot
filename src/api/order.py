from typing import List, Optional
from typing import Any
from dataclasses import dataclass

from src.api.cart import CartProduct
from src.client.client import HttpClient
from config import base_url


@dataclass
class Cart:
    id: int
    products: List[CartProduct]
    total_products: int
    final_price: str

    @staticmethod
    def from_dict(obj: Any) -> 'Cart':
        _id = int(obj.get("id"))
        _products = [CartProduct.from_dict(y) for y in obj.get("products")]
        _total_products = int(obj.get("total_products"))
        _final_price = str(obj.get("final_price"))
        return Cart(_id, _products, _total_products, _final_price)


@dataclass
class Customer:
    id: int
    tg_user_id: str
    first_name: str
    last_name: str
    phone: str
    address: str
    create_at: str

    @staticmethod
    def from_dict(obj: Any) -> 'Customer':
        _id = int(obj.get("id"))
        _tg_user_id = str(obj.get("tg_user_id"))
        _first_name = str(obj.get("first_name"))
        _last_name = str(obj.get("last_name"))
        _phone = str(obj.get("phone"))
        _address = str(obj.get("address"))
        _create_at = str(obj.get("create_at"))
        return Customer(_id, _tg_user_id, _first_name, _last_name, _phone, _address, _create_at)


@dataclass
class OrderData:
    id: int
    customer: Customer
    cart: Cart
    address: str
    status: str
    created_at: str

    @staticmethod
    def from_dict(obj: Any) -> 'OrderData':
        _id = int(obj.get("id"))
        _customer = Customer.from_dict(obj.get("customer"))
        _cart = Cart.from_dict(obj.get("cart"))
        _address = str(obj.get("address"))
        _status = str(obj.get("status"))
        _created_at = str(obj.get("created_at"))
        return OrderData(_id, _customer, _cart, _address, _status, _created_at)


def create_order(cart_id: str, address: str) -> Optional[OrderData]:
    headers = {
        "accept": "application/json",
    }
    cookies = {
        "cart_id": cart_id
    }
    url = base_url + "/api/v1/create-order/"
    client = HttpClient(
        url=url,
        headers=headers,
        json_data={"address": address},
        cookies=cookies
    )
    response = client.http_post_json()
    if not response or response.status_code != 201:
        return None
    return OrderData.from_dict(response.json())


def get_order(tg_user_id: str) -> List[dict]:
    headers = {
        "accept": "application/json",
        "tguserid": tg_user_id
    }
    url = base_url + "/api/v1/order/"
    client = HttpClient(
        url=url,
        headers=headers,
    )
    response = client.http_get()

    if not response or response.status_code != 200:
        return []
    data = response.json()
    return data

