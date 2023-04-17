from dataclasses import dataclass
from typing import Optional, List, Any

from src.api.category import Category
from src.client.client import HttpClient
from config import base_url


@dataclass
class Category:
    id: int
    name: str
    slug: str
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'Category':
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        _slug = str(obj.get("slug"))
        _url = str(obj.get("url"))
        return Category(_id, _name, _slug, _url)


@dataclass
class Product:
    id: int
    category: Category
    title: str
    url: str
    slug: str
    image: str
    description: str
    price: str

    @staticmethod
    def from_dict(obj: Any) -> 'Product':
        _id = int(obj.get("id"))
        _category = Category.from_dict(obj.get("category"))
        _title = str(obj.get("title"))
        _url = str(obj.get("url"))
        _slug = str(obj.get("slug"))
        _image = str(obj.get("image"))
        _description = str(obj.get("description"))
        _price = str(obj.get("price"))
        return Product(_id, _category, _title, _url, _slug, _image, _description, _price)


@dataclass
class CartProduct:
    id: int
    product: Product
    qty: float
    final_price: str

    @staticmethod
    def from_dict(obj: Any) -> 'CartProduct':
        _id = int(obj.get("id"))
        _product = Product.from_dict(obj.get("product"))
        _qty = float(obj.get("qty"))
        _final_price = str(obj.get("final_price"))
        return CartProduct(_id, _product, _qty, _final_price)


@dataclass
class CartProductResult:
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[CartProduct]

    @staticmethod
    def from_dict(obj: Any) -> 'CartProductResult':
        _count = int(obj.get("count"))
        _next = obj.get("next")
        _previous = obj.get("previous")
        _results = [CartProduct.from_dict(y) for y in obj.get("results")]

        return CartProductResult(_count, _next, _previous, _results)


@dataclass
class Cart:
    id: int
    products: List[CartProduct]
    total_products: float
    final_price: str

    @staticmethod
    def from_dict(obj: Any) -> 'Cart':
        _id = int(obj.get("id"))
        _products = [CartProduct.from_dict(y) for y in obj.get("products")]
        _total_products = float(obj.get("total_products"))
        _final_price = str(obj.get("final_price"))
        return Cart(_id, _products, _total_products, _final_price)


def get_cart(tg_user_id: str) -> Optional[Cart]:
    headers = {
        "accept": "application/json",
        "tguserid": tg_user_id
    }
    url = base_url + "/api/v1/cart/"
    client = HttpClient(
        url=url,
        headers=headers
    )
    response = client.http_get()
    if not response or response.status_code != 200:
        return None
    data = client.decode_json(response)
    if not data:
        return None

    cart = Cart.from_dict(data)
    return cart


def get_cart_products(tg_user_id: str, page) -> Optional[CartProductResult]:
    if page is None or page == "":
        page = "?page=1"
    headers = {
        "accept": "application/json",
        "tguserid": tg_user_id
    }
    url = base_url + f"/api/v1/cart-products/{page}"
    print(url)
    client = HttpClient(
        url=url,
        headers=headers
    )
    response = client.http_get()
    if not response or response.status_code != 200:
        return None
    data = client.decode_json(response)
    if not data:
        return None

    cart_product_result = CartProductResult.from_dict(data)
    return cart_product_result


def add_product_to_cart(cart_id: str, product_slug: str) -> bool:
    headers = {
        "accept": "application/json",
    }
    cookies = {
        "cart_id": cart_id
    }
    url = base_url + "/api/v1/add-to-cart/"
    client = HttpClient(
        url=url,
        headers=headers,
        json_data={"product_slug": product_slug},
        cookies=cookies
    )
    response = client.http_post_json()
    if not response or response.status_code != 200:
        return True
    return False


def delete_product_from_cart(cart_id: str, product_slug: str) -> bool:
    headers = {
        "accept": "application/json",
    }
    cookies = {
        "cart_id": cart_id
    }
    url = base_url + "/api/v1/delete-product-from-cart/"
    client = HttpClient(
        url=url,
        headers=headers,
        json_data={"product_slug": product_slug},
        cookies=cookies
    )
    response = client.http_post_json()
    if not response or response.status_code != 200:
        return False
    return True
