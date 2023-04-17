from pathlib import Path

from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types

from src.api.lang import get_customer_lang

I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, args):
        user = types.User.get_current()
        lang = get_customer_lang(str(user.id))
        return lang


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
