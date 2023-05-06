import os
import logging
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5997177755:AAFAN7RNcQFAS2g5aZjz1S32OQSyTgyf8Co'
YOOKASSA_TEST_PAYMENT_TOKEN = '381764678:TEST:54671'
ADMIN_ID = 405568659

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

accounts = []

PURCHASES_FILENAME = 'purchases.json'

if not os.path.exists(PURCHASES_FILENAME):
    with open(PURCHASES_FILENAME, 'w') as f:
        json.dump([], f)

try:
    with open('accounts.json', 'r') as file:
        accounts = json.load(file)
except FileNotFoundError:
    pass

PRICE = LabeledPrice(label="Аккаунт", amount=150 * 100)  # в копейках (руб)

@dp.callback_query_handler(lambda c: c.data == "clear_stats")
async def clear_stats(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != ADMIN_ID:
        return

    with open(PURCHASES_FILENAME, 'w') as f:
        json.dump([], f)

    await bot.answer_callback_query(callback_query.id, "Статистика успешно очищена.")
    await bot.send_message(callback_query.from_user.id, "Статистика успешно очищена.")




@dp.message_handler(commands=['stats'])
async def show_stats(message: types.Message):
    with open(PURCHASES_FILENAME, 'r') as f:
        purchases = json.load(f)
    total_sales = len(purchases)
    total_revenue = sum(purchase['amount'] for purchase in purchases)

    clear_stats_button = InlineKeyboardMarkup().add(InlineKeyboardButton("Стереть", callback_data="clear_stats"))
    
    await message.reply(f"Количество продаж: {total_sales}\nОбщая выручка: {total_revenue} руб.",
                        reply_markup=clear_stats_button)



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply('''Приветствую! Я бот магазина AI Avenue Shop🤖. 
    
Используй команду /buy_account, чтобы купить аккаунт ChatGPT.''')

@dp.message_handler(commands=['add_account'], commands_prefix='!')
async def cmd_add_account(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    account_info = message.text.split(' ', 1)[1].strip()
    accounts.append(account_info)

    with open('accounts.json', 'w') as file:
        json.dump(accounts, file)

    await message.reply(f"Аккаунт '{account_info}' успешно добавлен!")


@dp.message_handler(commands=['buy_account'])
async def buy(message: types.Message):
    if YOOKASSA_TEST_PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    if not accounts:
        await message.reply('''К сожалению, в настоящее время все аккаунты распроданы.
        
В скором времени мы добавим для вас новые аккаунты и вы снова сможете их преобрести. Для этого введите команду /buy_account чуть позже.''')
        return

    await bot.send_invoice(message.chat.id,
                           title="Аккаунт ChatGPT",
                           description=f'''Нажмите кнопку ниже чтобы оплатить аккаунт. 
После оплаты бот автоматически предоставит вам информацию об аккаунте.''',
                           provider_token=YOOKASSA_TEST_PAYMENT_TOKEN,
                           currency="rub",
                           photo_url="https://i.postimg.cc/4NWm7HFK/m-JI14-0-DOQ.jpg",
                           photo_width=450,
                           photo_height=450,
                           photo_size=450,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="account_purchase",
                           payload="test-invoice-payload")

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    global accounts
    account_info = accounts.pop(0)
    
    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно. \n\nИнформация об аккаунте:\n{account_info} \n\nОставьте хороший отзыв здесь: @aiavenuefaq")

    with open('accounts.json', 'w') as file:
        json.dump(accounts, file)

    if not accounts:
        with open('accounts.json', 'r') as file:
            accounts = json.load(file)
    
    with open(PURCHASES_FILENAME, 'r') as f:
        purchases = json.load(f)

    purchases.append({'amount': message.successful_payment.total_amount // 100})

    with open(PURCHASES_FILENAME, 'w') as f:
        json.dump(purchases, f)



@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Неверная команда. Используйте /help для получения списка доступных команд.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
