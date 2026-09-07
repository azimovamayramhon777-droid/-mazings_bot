import os
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# API kalitlarini muhit o'zgaruvchilaridan oladi
TELEGRAM_TOKEN = ("8953018034:AAEHQl1ZoSNPyrl4AThYVeY99zP1Zd6VtdM") 
OPENAI_API_KEY =("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") 

client = OpenAI(api_key=OPENAI_API_KEY)
,
# Foydalanuvchi ismlarini vaqtincha saqlash
user_names = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_names.pop(user_id, None)

    await update.message.reply_text(
        "Salom! 😎 Men hazilkash AI botman 😂\n\n"
        "Avval ismingizni ayting:"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Agar ism hali berilmagan bo'lsa
    if user_id not in user_names:
        user_names[user_id] = text

        # Komila uchun maxsus xabar
        if text.lower() == "komila":
            await update.message.reply_text(
                "Komila ❤️\n\n"
                "U sizga bu gaplarni aytishimni so‘radi… 💌\n"
                "U sizni sevishini yashira olmayapti. 🌹 "
                "Hatto sizni boshqalar bilan gaplashganingizni ko‘rsa, "
                "biroz rashk ham qiladi. 😊\n\n"
                "Eng qizig‘i, u sizni yanada ko‘proq hayajonga "
                "solishni xohlaydi… ❤️‍🔥\n"
                "Chunki uning uchun siz oddiy inson emassiz — "
                "siz alohida insonsiz. ✨"
            )
        else:
            await update.message.reply_text(
                f"{text} 😎 Zo‘r ism ekan! Endi savolingizni bering 😂"
            )

        return

    # Keyingi barcha xabarlarni AI javob beradi
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=(
                "Sen Telegramdagi hazilkash, do'stona AI botsan. "
                "Savollarga foydali va tushunarli javob ber. "
                "Javoblaringga o‘rinli, yengil hazil qo‘sh. "
                "Juda uzun yozma."
            ),
            input=text,
        )

        answer = response.output_text

        await update.message.reply_text(answer)

    except Exception as e:
        print("Xatolik:", e)
        await update.message.reply_text(
            "Voy 😅 Miyamga internet tiqilib qoldi shekilli. "
            "Yana bir marta yozib ko‘ring 😂"
        )


def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN topilmadi!")

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY topilmadi!")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot ishga tushdi! 🤖")
    app.run_polling()


if __name__ == "__main__":
    main()
