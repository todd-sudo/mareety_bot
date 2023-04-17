from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from config import ADMIN_CHAT_ID, LANGS
from src.api.check_user import check_user
from src.api.create_user import create_user
from src.api.lang import change_customer_lang
from src.handlers.keyboard import home_keyboard, main_menu_keyboard, \
    lang_keyboard, cansel_keyboard
from src.loader import dp, bot, _


class RegistrationState(StatesGroup):
    lang = State()
    first_name = State()
    last_name = State()
    phone = State()
    address = State()


class ReportState(StatesGroup):
    text_message = State()


class LangState(StatesGroup):
    lang = State()


start_message = "Привет!\n\nЯ бот Интернет-магазина mareety.com"


@dp.callback_query_handler(text="home")
async def home_handler(call: types.CallbackQuery):
    await call.answer(_("Информация загружается"))
    user_lang = check_user(str(call.from_user.id))
    if user_lang:
        keyboard = main_menu_keyboard(user_lang)
        await call.message.answer(text=_("Главное меню"), reply_markup=keyboard, disable_notification=True)


@dp.callback_query_handler(text="report")
async def report_handler(call: types.CallbackQuery):
    await call.answer(_("Информация загружается"))
    await call.message.answer(_("Введите текст вопроса"), disable_notification=True)
    await ReportState.text_message.set()


@dp.message_handler(state=ReportState.text_message)
async def add_text_message_state(message: types.Message, state: FSMContext):
    text_message = message.text
    if text_message == _("Отмена"):
        await message.answer(
            text=_("Действите отменено"), reply_markup=home_keyboard(), disable_notification=True
        )
        await state.reset_state()
        return
    await state.finish()
    msg = _(
        "Вопрос от пользователя @{0}\n\nText:\n{1}"
        .format(
            message.from_user.username, text_message
        )
    )
    await bot.send_message(ADMIN_CHAT_ID, msg)
    await message.answer(
        _("Ваш вопрос отправлен! Оператор с Вами свяжется."),
        reply_markup=home_keyboard(),
        disable_notification=True
    )


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_lang = check_user(str(message.from_user.id))
    if user_lang:
        keyboard = main_menu_keyboard(user_lang)
        await message.answer(text=_(start_message), reply_markup=keyboard, disable_notification=True)
        return
    else:
        await message.answer(_('Выберите язык', locale="uz"), reply_markup=lang_keyboard("uz"), disable_notification=True)
        await RegistrationState.lang.set()


@dp.message_handler(state=RegistrationState.lang)
async def add_lang_state(message: types.Message, state: FSMContext):
    global lang_str
    lang_str = message.text
    if lang_str == _("Отмена", locale=lang_str):
        await state.reset_state()
        await RegistrationState.lang.set()
        return
    if lang_str not in LANGS:
        await state.reset_state()
        await RegistrationState.lang.set()
    else:
        await state.update_data(answer1=lang_str)
        await message.answer(_('Введите имя', locale=lang_str), reply_markup=cansel_keyboard(lang_str), disable_notification=True)
        await RegistrationState.first_name.set()


@dp.message_handler(state=RegistrationState.first_name)
async def add_first_name_state(message: types.Message, state: FSMContext):
    global first_name
    first_name = message.text
    if first_name == _("Отмена", locale=lang_str):
        await message.answer(
            text=_("Отмена регистрации\n\nВведите /start чтобы начать заново", locale=lang_str), disable_notification=True
        )
        await state.reset_state()
        return
    await state.update_data(answer1=first_name)
    await message.answer(_('Введите фамилию', locale=lang_str), reply_markup=cansel_keyboard(lang_str), disable_notification=True)
    await RegistrationState.last_name.set()


@dp.message_handler(state=RegistrationState.last_name)
async def add_last_name_state(message: types.Message, state: FSMContext):
    global last_name
    last_name = message.text
    if last_name == _("Отмена", locale=lang_str):
        await message.answer(
            text=_("Отмена регистрации\n\nВведите /start чтобы начать заново", locale=lang_str), disable_notification=True
        )
        await state.reset_state()
        return
    await state.update_data(answer1=last_name)
    keyboard = cansel_keyboard(lang_str)
    keyboard.add(
        types.KeyboardButton(
            text=_("Отправить номер телефона 📱", locale=lang_str),
            request_contact=True
        )
    )
    await message.answer(
        _('Введите телефон', locale=lang_str), reply_markup=keyboard, disable_notification=True
    )
    await RegistrationState.phone.set()


@dp.message_handler(state=RegistrationState.phone, content_types=[types.ContentType.TEXT, types.ContentType.CONTACT])
async def add_phone_state(message: types.Message, state: FSMContext):
    global phone
    if message.content_type in [types.ContentType.CONTACT, types.ContentType.TEXT]:
        phone = message.contact
        if phone:
            phone = phone.phone_number
        else:
            phone = message.text.strip()
        if phone == _("Отмена", locale=lang_str):
            await message.answer(
                text=_("Отмена регистрации\n\nВведите /start чтобы начать заново", locale=lang_str),
                disable_notification=True
            )
            await state.reset_state()
            return
        await state.update_data(answer1=phone)
        await message.answer(_('Введите адрес', locale=lang_str), reply_markup=cansel_keyboard(lang_str), disable_notification=True)
        await RegistrationState.address.set()


@dp.message_handler(state=RegistrationState.address)
async def add_address_state(message: types.Message, state: FSMContext):
    address = message.text
    if address == _("Отмена", locale=lang_str):
        await message.answer(
            text=_("Отмена регистрации\n\nВведите /start чтобы начать заново", locale=lang_str),
            disable_notification=True
        )
        await state.reset_state()
        return
    await state.update_data(answer1=address)

    user = create_user(
        tg_user_id=str(message.from_user.id),
        first_name=str(first_name),
        last_name=str(last_name),
        phone=str(phone),
        address=address,
        lang=lang_str,
    )
    if user:
        await bot.send_message(
            ADMIN_CHAT_ID,
            _(
                "Добавлен новый пользователь @{0}. Номер телефона: {1}!".format(
                    message.from_user.username, phone
                ),
                locale=lang_str
            )
        )
        keyboard = main_menu_keyboard(lang_str)
        await message.answer(
            text=_(start_message, locale=lang_str), reply_markup=keyboard, disable_notification=True
        )
        await state.finish()
        # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # keyboard.add(types.KeyboardButton(
        #     text=_("Отправить номер телефона 📱", locale=lang_str),
        #     request_contact=True)
        # )
        #
        # await message.answer(
        #     _("Отправь свой контакт:", locale=lang_str),
        #     reply_markup=keyboard
        # )
        # await RegistrationState.contact.set()
    else:
        await state.reset_state()
        await message.answer(text=_("Ошибка регистрации", locale=lang_str), disable_notification=True)


# @dp.message_handler(
#     state=RegistrationState.contact, content_types=types.ContentType.CONTACT
# )
# async def add_contact_state(message: types.Message, state: FSMContext):
#     contact_phone = message.contact.phone_number
#     await message.answer(
#         _(
#             "Твой номер успешно получен: {0}".format(
#                 contact_phone
#             ),
#             locale=lang_str
#         ),
#         reply_markup=types.ReplyKeyboardRemove()
#     )
#     await bot.send_message(
#         ADMIN_CHAT_ID,
#         _(
#             "Добавлен новый пользователь @{0}. Номер телефона: {1}!".format(
#                 message.from_user.username, contact_phone
#             ),
#             locale=lang_str
#         )
#     )
#     keyboard = main_menu_keyboard(lang_str)
#     await message.answer(
#         text=_(start_message, locale=lang_str), reply_markup=keyboard
#     )
#     await state.finish()


@dp.callback_query_handler(text="lang")
async def change_language(call: types.CallbackQuery):
    await call.answer(_("Изменение языка"))
    await call.message.answer(_("Выберите язык"), reply_markup=lang_keyboard(""), disable_notification=True)
    await LangState.lang.set()


@dp.message_handler(state=LangState.lang)
async def add_lang_state(message: types.Message, state: FSMContext):
    lang = message.text
    if lang == _("Отмена"):
        await state.finish()
        await message.answer(_("Действие отменено"), reply_markup=home_keyboard(""), disable_notification=True)
    if lang not in LANGS:
        await state.reset_state()
        await message.answer(
            _("Нет такого варианта"), reply_markup=home_keyboard(), disable_notification=True
        )
    status = change_customer_lang(str(message.from_user.id), lang)
    if status != 200:
        await message.answer(_("Произошла ошибка"), reply_markup=home_keyboard(), disable_notification=True)
    else:
        await message.answer(
            _("Язык успешно изменен"), reply_markup=types.ReplyKeyboardRemove(), disable_notification=True
        )
    await message.answer(
        _("Меню"), reply_markup=home_keyboard(), disable_notification=True
    )
    await state.finish()

