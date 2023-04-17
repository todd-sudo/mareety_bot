import time

from aiogram import types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from config import ADMIN_CHAT_ID
from src.api.cart import get_cart
from src.api.order import get_order, create_order, OrderData
from src.handlers.keyboard import home_keyboard
from src.loader import dp, bot, _


class CreateOrderState(StatesGroup):
    address = State()


@dp.callback_query_handler(text="orders")
async def get_orders_handler(call: types.CallbackQuery):
    await call.answer(_("Информация загружается"))
    orders_data = get_order(str(call.from_user.id))
    if not orders_data:
        await call.message.answer(
            _("У вас нет заказов"), reply_markup=home_keyboard(), disable_notification=True
        )
        return
    for order_data_json in orders_data:
        order_data = OrderData.from_dict(order_data_json)
        cart_products = order_data.cart.products
        final_price = order_data.cart.final_price
        total_products = len(cart_products)
        status_order = order_data.status
        address = order_data.address
        created_at = order_data.created_at

        base_msg = _("""
Заказ №{0}

Всего товаров: {1}
Итоговая цена: {2} UZS
Статус заказа: {3}
Город: {4}
Дата заказа: {5}
""".format(
            order_data.id,
            hbold(str(int(total_products))),
            hbold(str(final_price)),
            status_order,
            address,
            created_at
        ))
        await call.message.answer(base_msg, disable_notification=True)
        if not cart_products:
            await call.message.answer(base_msg, disable_notification=True)
            return

        for item in cart_products:
            item_product = item.product
            item_url = item_product.url
            msg = """
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
            if item_url:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text=_("Посмотреть на сайте"),
                        url=item_url
                    )
                )
            keyboard.add(
                types.InlineKeyboardButton(
                    text=_("Домой"),
                    callback_data="home"
                )
            )
            await call.message.answer(text=_(msg), reply_markup=keyboard, disable_notification=True)
            time.sleep(0.5)


@dp.callback_query_handler(text="create_order")
async def create_order_handler(call: types.CallbackQuery):
    await call.answer(_("Информация загружается"))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(_("Отмена"))
    await call.answer(_("Начало создания заказа"))
    await call.message.answer(_('Введите адрес'), reply_markup=keyboard, disable_notification=True)
    await CreateOrderState.address.set()


@dp.message_handler(state=CreateOrderState.address)
async def add_address_order_state(message: types.Message, state: FSMContext):
    address = message.text
    if address == _("Отмена"):
        await state.reset_state()
        await message.answer(
            _("Создание заказа отменено"),
            reply_markup=home_keyboard(),
            disable_notification=True
        )
        return
    await state.update_data(answer1=address)
    cart = get_cart(str(message.from_user.id))
    cart_id = str(cart.id)
    order_data = create_order(cart_id, address)
    cart_products = order_data.cart.products
    final_price = order_data.cart.final_price
    total_products = len(cart_products)
    status_order = order_data.status
    address = order_data.address
    created_at = order_data.created_at

    base_msg = _("""
Заказ №{0}

Всего товаров: {1}
Итоговая цена: {2} UZS
Статус заказа: {3}
Город: {4}
Дата заказа: {5}
""".format(
        order_data.id,
        hbold(str(int(total_products))),
        hbold(str(final_price)),
        status_order,
        address,
        created_at
    ))
    if not cart_products:
        await message.answer(base_msg, reply_markup=home_keyboard(), disable_notification=True)
        return
    await message.answer(text=base_msg, disable_notification=True)
    for item in cart_products:
        item_product = item.product
        item_url = item_product.url
        msg = """
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
        if item_url:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=_("Посмотреть на сайте"),
                    url=item_url
                )
            )
        keyboard.add(
            types.InlineKeyboardButton(text=_("Домой"), callback_data="home")
        )
        await message.answer(text=_(msg), reply_markup=keyboard, disable_notification=True)
        time.sleep(0.5)
    await state.finish()

    await bot.send_message(
        ADMIN_CHAT_ID,
        _("Пользователь @{0} оформил заказ.\nНомер заказа {1}".format(
            message.from_user.username, order_data.id
        ))
    )
