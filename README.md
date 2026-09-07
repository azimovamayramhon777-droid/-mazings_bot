import asyncio
import os
from aiogram import Bot, Dispatcher, types
import google.generativeai as genai

# Environment variablalardan olamiz
API_TOKEN = os.getenv('8953018034:AAEHQl1ZoSNPyrl4AThYVeY99zP1Zd6VtdM')
GEMINI_API_KEY = os.getenv('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')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

SYSTEM_INSTRUCTION = """
Siz Telegram botdagi juda aqlli, muloyim va do'stona Sun'iy Intellekt yordamchisiz.
Javoblaringiz o'zbek tilida, aniq va samimiy bo'lsin.

MUHIM QAIDA:
Agar foydalanuvchi o'z ismini "Komila" yoki "Kamila" deb kiritsa:
Unga juda chiroyli, shirin va samimiy tarzda uni sevishini, qadrli ekanligini aytib o'ting.

Boshqa savollar uchun odatiy, aqlli javob bering.
"""

def get_ai_response(text: str) -> str:
    try:
        response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\nFoydalanuvchi: {text}")
        return response.text or "Javob olib bo'lmadi."
    except Exception as e:
        print(f"Xato: {e}")
        return "Texnik muammo bor. Iltimos qayta urinib ko'ring. 😅"

@dp.message(lambda message: message.text == "/start")
async def start_command(message: types.Message):
    await message.answer("Salom! 👋 Men AI yordamchiman. Ismingizni yoki savolingizni yozing!")

@dp.message()
async def handle_all_messages(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    ai_reply = get_ai_response(message.text)
    await message.answer(ai_reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
