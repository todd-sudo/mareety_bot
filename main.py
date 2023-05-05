
from aiogram import executor

from src.loader import bot, dp
from logger import logger
from src import handlers


async def on_startup(_):
    logger.success("Start Bot")
    # await bot.delete_webhook()


async def on_shutdown(dp):
    logger.info("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info("Bot down")


if __name__ == '__main__':
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False
    )
