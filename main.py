import os
from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.getenv("BOT_TOKEN")  # безопасно из переменной окружения
GROUP_ID = -1001523628023  # ID приватной группы
ADMIN_USERNAME = "@LowDropSeeds"
KASPI_REKVIZITY = "4400430262247957"
SUBSCRIPTION_COST = "10 000 ₸"
GROUP_LINK = "https://t.me/+dgd0Hm2v6603MjRi"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопка "Отправить чек"
def get_check_button():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Отправить чек", callback_data="send_check"))
    return kb

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    chat_member = await bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)

    if chat_member.status in ("member", "creator", "administrator"):
        await message.answer("Вы уже подписаны. Добро пожаловать!")
    else:
        text = (
            f"Подписка стоит {SUBSCRIPTION_COST} в год.\n"
            f"Оплатите на Kaspi: `{KASPI_REKVIZITY}`\n"
            f"Затем отправьте чек администратору: {ADMIN_USERNAME}\n"
            f"После проверки вы получите доступ в закрытую группу.\n"
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=get_check_button())

@dp.callback_query_handler(lambda c: c.data == "send_check")
async def handle_send_check(callback: types.CallbackQuery):
    await callback.message.answer(
        f"Пожалуйста, отправьте чек об оплате администратору: {ADMIN_USERNAME}\n"
        f"После одобрения вы получите доступ: {GROUP_LINK}"
    )
    await callback.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
