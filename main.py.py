
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils import executor
import logging

API_TOKEN = '7816793414:AAHpc-nEWLeJiZWQGhBcPc9M9OJg_WyoF5Q'
GROUP_ID = -1001523628023
PRIVATE_GROUP_LINK = 'https://t.me/+dgd0Hm2v6603MjRi'
ADMIN_USERNAME = '@LowDropSeeds'
KASPI_REQUISITES = '4400 4302 6224 7957 (Kaspi Gold)'
SUBSCRIPTION_PRICE = '10 000₸ в год'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Кнопки
pay_button = InlineKeyboardButton(text="Оплатить подписку", callback_data="pay_subscription")
send_check_button = InlineKeyboardButton(text="Отправить чек", switch_inline_query_current_chat="Отправляю чек: ")
subscription_keyboard = InlineKeyboardMarkup().add(pay_button).add(send_check_button)

async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@dp.message_handler(commands=['start'])
@dp.message_handler()
async def handle_message(message: Message):
    user_id = message.from_user.id

    if await is_subscribed(user_id):
        await message.answer(
            "Вы уже подписаны на закрытую группу *LowDropSeeds*!

"
            "Доступен пробный товар:
"
            "*Арбуз Hollar Select* — *17 000₸*

"
            "Оплата через Kaspi:
"
            f"`{KASPI_REQUISITES}`

"
            f"После оплаты пришлите чек сюда или напишите {ADMIN_USERNAME}.",
            parse_mode='Markdown',
            reply_markup=subscription_keyboard
        )
    else:
        await message.answer(
            f"Для доступа к магазину необходима подписка: *{SUBSCRIPTION_PRICE}*",
            parse_mode='Markdown',
            reply_markup=subscription_keyboard
        )

@dp.callback_query_handler(lambda call: call.data == "pay_subscription")
async def handle_pay_callback(call: CallbackQuery):
    await call.message.answer(
        "*Информация для оплаты:*

"
        f"Сумма: *{SUBSCRIPTION_PRICE}*
"
        f"Kaspi: `{KASPI_REQUISITES}`

"
        f"После оплаты отправьте чек сюда или админу: {ADMIN_USERNAME}
"
        f"После проверки вы получите доступ в группу:
{PRIVATE_GROUP_LINK}

"
        "_Вход доступен только после одобрения администратора._",
        parse_mode='Markdown'
    )
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
