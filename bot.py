import os
import random
from datetime import time
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN غير موجود. أضفه إلى ملف .env")

if not TARGET_CHAT_ID:
    raise ValueError("TARGET_CHAT_ID غير موجود. أضفه إلى ملف .env")


def get_random_ayah():
    try:
        ayah_id = random.randint(1, 6236)
        url = f"https://api.alquran.cloud/v1/ayah/{ayah_id}/editions/ar.alafasy"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()["data"][0]

        text = data["text"]
        surah_name = data["surah"]["name"]
        surah_number = data["surah"]["number"]
        ayah_number = data["numberInSurah"]

        return (
            "🕌 آية اليوم\n\n"
            f"📖 {text}\n\n"
            f"📚 السورة: {surah_name}\n"
            f"🔢 رقم الآية: {ayah_number}\n"
            f"🧾 رقم السورة: {surah_number}"
        )
    except Exception as e:
        return f"حدث خطأ أثناء جلب الآية: {e}"


async def send_verse(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data
    message = get_random_ayah()
    await context.bot.send_message(chat_id=chat_id, text=message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً 👋\n\n"
        "أنا بوت الآيات اليومية من المصحف.\n\n"
        "الأوامر المتاحة:\n"
        "/start - بدء البوت\n"
        "/ayah - آية عشوائية\n"
        "/help - قائمة الأوامر"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def ayah_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_random_ayah())


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ayah", ayah_command))

    job_queue = app.job_queue
    target_chat_id = int(TARGET_CHAT_ID)

    job_queue.run_daily(
        send_verse,
        time=time(hour=8, minute=0, tzinfo=ZoneInfo("Asia/Riyadh")),
        days=(0, 1, 2, 3, 4, 5, 6),
        data=target_chat_id,
    )

    job_queue.run_daily(
        send_verse,
        time=time(hour=18, minute=0, tzinfo=ZoneInfo("Asia/Riyadh")),
        days=(0, 1, 2, 3, 4, 5, 6),
        data=target_chat_id,
    )

    print("✅ البوت يعمل...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
