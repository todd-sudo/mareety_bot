from aiogram import types

from config import base_url
from src.loader import _


def lang_keyboard(locale: str = "uz"):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(
        _("en", locale=locale),
        _("uz", locale=locale),
        _("ru", locale=locale),
        _("Отмена", locale=locale)
    )
    return keyboard


def cansel_keyboard(lang_str: str = "uz"):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(
        _("Отмена", locale=lang_str)
    )
    return keyboard


def main_menu_keyboard(locale: str = "uz"):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text=_("Каталог", locale=locale), callback_data="catalog"
    ))
    keyboard.add(types.InlineKeyboardButton(
        text=_("Корзина", locale=locale), callback_data="cart"
    ))
    keyboard.add(
        types.InlineKeyboardButton(
            text=_("Сделать заказ", locale=locale), callback_data="create_order"
        ),
        types.InlineKeyboardButton(
            text=_("Мои заказы", locale=locale), callback_data="orders"
        )
    )
    keyboard.add()
    keyboard.add(types.InlineKeyboardButton(
        text=_("Задать вопрос", locale=locale), callback_data="report"
    ))
    keyboard.add(types.InlineKeyboardButton(
        text=_("Язык", locale=locale), callback_data="lang"
    ))
    return keyboard


def pagination_keyboard_product(
        keyboard: types.InlineKeyboardMarkup,
        _cb,
        _next: str,
        _previous: str,
        category_id: str,
) -> types.InlineKeyboardMarkup:
    str_replace = base_url + f"/api/v1/product-list/{category_id}/"

    if _previous:
        _previous = _previous.replace(str_replace, "")
        if not _previous:
            _previous = ""
        c_pk_page = _previous + "__" + category_id
        keyboard.add(
            types.InlineKeyboardButton(
                text="⬅️ " + _("Назад"), callback_data=_cb.new(
                    c_pk_page=c_pk_page
                )
            )
        )
    if _next:
        _next = _next.replace(str_replace, "")
        if not _next:
            _next = ""
        c_pk_page = _next + "__" + category_id
        keyboard.add(
            types.InlineKeyboardButton(
                text=_("Вперед") + " ➡️", callback_data=_cb.new(
                    c_pk_page=c_pk_page
                )
            )
        )

    return keyboard


def pagination_keyboard_cart(
        keyboard: types.InlineKeyboardMarkup,
        _cb,
        _next: str,
        _previous: str,
        cart_id: str,
) -> types.InlineKeyboardMarkup:
    str_replace = base_url + f"/api/v1/cart-products/"
    if _previous:
        _previous = _previous.replace(str_replace, "")
        if not _previous:
            _previous = ""
        cp_pk_cart = _previous + "__" + cart_id
        keyboard.add(
            types.InlineKeyboardButton(
                text="⬅️ " + _("Назад"), callback_data=_cb.new(
                    cp_pk_cart=cp_pk_cart
                )
            )
        )
    if _next:
        _next = _next.replace(str_replace, "")
        if not _next:
            _next = ""
        cp_pk_cart = _next + "__" + cart_id
        keyboard.add(
            types.InlineKeyboardButton(
                text=_("Вперед") + " ➡️", callback_data=_cb.new(
                    cp_pk_cart=cp_pk_cart
                )
            )
        )

    return keyboard


def home_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text=_("Домой"), callback_data="home")
    )
    return keyboard
