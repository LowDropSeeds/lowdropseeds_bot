
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import logging

API_TOKEN = '7816793414:AAFEjtplK0535pjj2DdIk2sZXdiNI-_gPMA'
GROUP_ID = -1002596106011  # ID приватной группы LowDropSeeds

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("Связаться с продавцом", url="https://t.me/LowDropSeeds"))
            await message.answer(
                "🟢 *Hollar Select* — 17 000 тг\n\n"
                "Для оформления заказа:\n"
                "1. Напишите продавцу: @LowDropSeeds\n"
                "2. Оплатите через Kaspi\n"
                "3. Закажите доставку\n\n"
                "Спасибо за покупку!",
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        else:
            await message.answer("❌ Для доступа к товару необходимо быть участником группы LowDropSeeds.")
    except Exception as e:
        await message.answer("❌ Ошибка при проверке подписки. Попробуйте позже.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
