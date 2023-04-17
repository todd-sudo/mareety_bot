import time
from typing import Optional

from aiogram import types
from aiogram.utils.markdown import hbold, hlink

from src.api.cart import get_cart_products, get_cart, delete_product_from_cart
from src.handlers.callback import n_p_cart_product, \
    cb_change_qty_cart_product, del_cart_product
from src.handlers.keyboard import pagination_keyboard_cart, home_keyboard
from src.loader import dp, bot, _


async def _get_cart_products_from_api(
        call: types.CallbackQuery, page: Optional[str]
):

    if page:
        page = page.split("__")[0]

    cart_product_result = get_cart_products(str(call.from_user.id), page)
    cart = get_cart(str(call.from_user.id))
    print(cart.id)
    if not cart:
        await call.message.answer(
            _("Ваша корзина пуста!"), reply_markup=home_keyboard(), disable_notification=True
        )
        return
    base_msg = """
Всего товаров: {0}
Итоговая цена: {1} UZS
""".format(
        hbold(str(int(cart.total_products))),
        hbold(str(cart.final_price))
    )

    _next = cart_product_result.next
    _previous = cart_product_result.previous

    products = cart_product_result.results
    if not products:
        await call.message.answer(_(base_msg), disable_notification=True)
        return

    len_products = len(products)
    index = 0
    for item in products:
        item_product = item.product
        index += 1
        item_url = item_product.url
        (msg) = """
{0} {1}

{2}
{3} UZS
{4}
""".format(
            hlink("🖥", item_product.image),
            item_product.category.name,
            hlink(item_product.title, item_url),
            item_product.price,
            item_product.description
        )
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        cart_alias = f"{item_product.slug}==={cart.id}"
        if item_url:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=_("Посмотреть на сайте"),
                    url=item_url
                )
            )
        keyboard.add(
            types.InlineKeyboardButton(
                text=_("Удалить из корзины"),
                callback_data=del_cart_product.new(
                    cart_alias=cart_alias
                )
            )
        )
        if index == len_products:
            reply_markup = pagination_keyboard_cart(
                    keyboard,
                    n_p_cart_product,
                    _next,
                    _previous,
                    str(cart.id),
                )
            reply_markup.add(
                types.InlineKeyboardButton(text=_("Домой"), callback_data="home")
            )
            await call.message.answer(
                text=_(msg),
                reply_markup=reply_markup,
                parse_mode=types.ParseMode.HTML,
                disable_notification=True
            )
            return
        await call.message.answer(text=_(msg), reply_markup=keyboard, disable_notification=True)
        time.sleep(0.5)


@dp.callback_query_handler(n_p_cart_product.filter())
async def next_previous_product_from_cart_handler(
        call: types.CallbackQuery, callback_data: dict
):
    page = callback_data.get("cp_pk_cart", None)
    await _get_cart_products_from_api(call, page)


@dp.callback_query_handler(del_cart_product.filter())
async def delete_product_from_cart_handler(
        call: types.CallbackQuery, callback_data: dict
):
    cart_alias = callback_data.get("cart_alias", None)
    if cart_alias:
        cart_alias = cart_alias.split("===")
        product_slug = cart_alias[0]
        cart_id = cart_alias[1]
        cart_deleted = delete_product_from_cart(cart_id, product_slug)
        if cart_deleted:
            await bot.delete_message(
                call.message.chat.id, call.message.message_id
            )
            await call.answer(_("Успешно удалено"))
            return
        else:
            await call.message.answer(
                _("Произошла ошибка удаления"), reply_markup=home_keyboard(), disable_notification=True
            )
            return
    await call.message.answer(_("Произошла ошибка"), reply_markup=home_keyboard(), disable_notification=True)


@dp.callback_query_handler(text="cart")
async def get_cart_products_handler(call: types.CallbackQuery):
    await call.answer(_("Информация загружается"))
    await _get_cart_products_from_api(call, None)
