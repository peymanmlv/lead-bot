import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatType
from aiohttp import web

API_TOKEN = "7884991015:AAG2MVTzcPIAw0CQ-x3l7Qgf2KRyUyu9yd4"
ADMIN_ID = 443143385  # آیدی عددی خودت

WEBHOOK_PATH = "/webhook"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message()
async def monitor(message: types.Message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return
    if not message.text:
        return

    text = message.text
    keywords = ["قیمت", "خرید", "چنده", "مشاوره"]

    if not any(k in text for k in keywords):
        return

    user = message.from_user

    await bot.send_message(
        ADMIN_ID,
        f"""📥 لید جدید
👤 {user.full_name}
🆔 {user.id}
💬 {text}
"""
    )

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)

async def on_shutdown(app):
    await bot.delete_webhook()

app = web.Application()
app.router.add_post(WEBHOOK_PATH, dp.webhook_handler(bot))
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, port=3000)
