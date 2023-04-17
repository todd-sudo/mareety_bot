import time

from aiogram import types

from src.api.cart import get_cart_products, add_product_to_cart, get_cart
from src.api.category import get_categories
from src.api.product import get_product_list_by_category_id, parse_product
from src.handlers.callback import cb_categories, cb_cart
from src.handlers.keyboard import pagination_keyboard_product, home_keyboard
from src.loader import dp, bot, _


@dp.callback_query_handler(text="catalog")
async def get_categories_handler(call: types.CallbackQuery):
    await call.answer(_("Информация загружается"))
    categories = get_categories()
    if not categories:
        await call.message.answer(_("Нет данных!"), disable_notification=True)
        return
    keyboard = types.InlineKeyboardMarkup()

    for c in categories:
        keyboard.add(types.InlineKeyboardButton(
            text=c.name,
            callback_data=cb_categories.new(c_pk_page=" __" + str(c.pk))
        ))
    keyboard.add(
        types.InlineKeyboardButton(
            text=_("Домой"),
            callback_data="home"
        )
    )
    await call.message.answer(_("Категории:"), reply_markup=keyboard, disable_notification=True)


@dp.callback_query_handler(cb_categories.filter())
async def get_products_by_category_id_handler(
        call: types.CallbackQuery, callback_data: dict
):
    await call.answer(_("Информация загружается"))
    cart_id = get_cart(str(call.from_user.id)).id
    cb_data = callback_data["c_pk_page"].split("__")
    category_id = cb_data[1]
    page = cb_data[0]
    if page == " ":
        page = "?page=1"
    data = get_product_list_by_category_id(category_id, page)
    if not data:
        await call.message.answer(
            _("🆘 Произошла ошибка получения данных!"),
            reply_markup=home_keyboard()
        )
        return
    _next = data.get("next")
    _previous = data.get("previous")
    products = data.get("results")
    if products:
        len_products = len(products)
        index = 0
        for item in products:
            index += 1
            item_url = item.get("url")
            msg, slug = parse_product(item)
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            cart_alias = f"{slug}==={cart_id}"
            if item_url:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=_("Посмотреть на сайте"),
                        url=item_url
                    )
                )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=_("🛍 Добавить в корзину"),
                    callback_data=cb_cart.new(t_cart=cart_alias)
                )
            )
            if index == len_products:
                reply_markup = pagination_keyboard_product(
                        keyboard,
                        cb_categories,
                        _next,
                        _previous,
                        category_id,
                    )
                reply_markup.add(
                    types.InlineKeyboardButton(
                        text=_("Домой"),
                        callback_data="home"
                    )
                )
                await call.message.answer(
                    text=_(msg),
                    reply_markup=reply_markup,
                    parse_mode=types.ParseMode.HTML,
                    disable_notification=True
                )
                return
            keyboard.add(
                types.InlineKeyboardButton(
                    text=_("Домой"),
                    callback_data="home"
                )
            )
            await call.message.answer(text=_(msg), reply_markup=keyboard, disable_notification=True)
            time.sleep(0.5)
    else:
        await call.message.answer(
            text=_("❌ Нет данных"), reply_markup=home_keyboard(), disable_notification=True
        )


@dp.callback_query_handler(cb_cart.filter())
async def add_to_cart_handler(call: types.CallbackQuery, callback_data: dict):
    await call.answer(_("Информация загружается"))
    cb_data = callback_data.get("t_cart").split("===")
    slug = cb_data[0]
    cart_id = cb_data[1]
    cart = add_product_to_cart(cart_id, slug)
    if cart:
        await call.message.edit_text(
            _("Товар добавлен в корзину"), reply_markup=home_keyboard()
        )
        return
    await call.message.answer(
        _("Произошла ошибка добавления товара в корзину"),
        reply_markup=home_keyboard(),
        disable_notification=True
    )


@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    msg = f"chat_id: {message.chat.id}\n"\
          f"user_id: {message.from_user.id}\n"\
          f"username: {message.from_user.username}"
    await message.answer(
        text=_(msg),
        disable_notification=True
    )
