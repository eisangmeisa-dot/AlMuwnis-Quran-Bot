BOT_TOKEN=ضع_الـ_Token_هنا
TARGET_CHAT_ID=-1001234567890import requests
import random

def get_random_ayah():
    ayah_id = random.randint(1, 6236)
    url = f"https://api.alquran.cloud/v1/ayah/{ayah_id}/editions/ar.alafasy"
    r = requests.get(url, timeout=10)
    data = r.json()["data"][0]

    text = data["text"]
    surah = data["surah"]["name"]
    ayah_no = data["numberInSurah"]
    surah_no = data["surah"]["number"]

    return f"""
🕌 آية اليوم

📖 {text}

📚 السورة: {surah}
🔢 رقم الآية: {ayah_no}
🧾 رقم السورة: {surah_no}
"""TARGET_CHAT_ID=-1001234567890BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TARGET_CHAT_ID=-1001234567890pip install python-telegram-bot apscheduler requests python-dotenv/tafsir
/surah
/ayahpython bot.pypip install python-telegram-bot apscheduler requestsimport requests
import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# -----------------------------
# إعدادات البوت
# -----------------------------
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"  # مثال: -1001234567890

# -----------------------------
# جلب آية قرآنية عشوائية
# -----------------------------
def get_random_quran_ayah():
    try:
        ayah_id = random.randint(1, 6236)  # عدد آيات القرآن
        url = f"https://api.alquran.cloud/v1/ayah/{ayah_id}/editions/ar.alafasy"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        ayah = data["data"][0]

        text = ayah["text"]
        surah_name = ayah["surah"]["name"]
        surah_number = ayah["surah"]["number"]
        ayah_number = ayah["numberInSurah"]

        return f"""
🕌 آية اليوم

📖 {text}

📚 السورة: {surah_name}
🔢 رقم الآية: {ayah_number}
🧾 رقم السورة: {surah_number}
"""
    except Exception as e:
        return f"حدث خطأ أثناء جلب الآية: {str(e)}"

# -----------------------------
# إرسال الآية
# -----------------------------
async def send_daily_verse(context: ContextTypes.DEFAULT_TYPE):
    msg = get_random_quran_ayah()
    await context.bot.send_message(chat_id=CHAT_ID, text=msg)

# -----------------------------
# أمر يدوي
# -----------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا! البوت جاهز، وسيتم إرسال آية يومية تلقائيًا كل يوم في الساعة 08:00."
    )

# -----------------------------
# تشغيل البوت
# -----------------------------
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        __import__("telegram.ext").ext.CommandHandler("start", start_command)
    )

    scheduler = AsyncIOScheduler(timezone="Asia/Riyadh")
    scheduler.add_job(send_daily_verse, "cron", hour=8, minute=0, args=[app])
    scheduler.start()

    print("✅ البوت يعمل...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())import requests
import schedule
import time
from telegram import Bot
from telegram.error import TelegramError
import logging

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN)

def get_random_quran_verse():
    """جلب آية عشوائية من API القرآن"""
    try:
        response = requests.get("http://api.alquran.cloud/v1/randomaya")
        if response.status_code == 200:
            data = response.json()
            ayah = data['data']
            return {
                "text": ayah['text'],
                "surah": ayah['surah']['name'],
                "number": ayah['numberInSurah']
            }
    except Exception as e:
        logger.error(f"خطأ في API: {e}")
    return None

def send_daily_verse():
    """إرسال آية يومية"""
    verse = get_random_quran_verse()
    
    if verse:
        message = f"""
🕌 *آية اليوم*

📖 *{verse['text']}*

📚 *السورة:* {verse['surah']}
📍 *رقم الآية:* {verse['number']}
        """
        try:
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
            logger.info("✅ تم إرسال الآية")
        except TelegramError as e:
            logger.error(f"❌ خطأ: {e}")

def schedule_messages():
    schedule.every().day.at("08:00").do(send_daily_verse)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logger.info("🤖 البوت يعمل...")
    schedule_messages()python quran_bot.pyimport logging
from telegram import Bot
from telegram.error import TelegramError
import schedule
import time
from datetime import datetime
import requests
import threading

# ضع Token بوتك هنا
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"  # معرف القناة أو الجروب

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)

# قائمة بآيات قرآنية
QURAN_VERSES = [
    {
        "verse": "بسم الله الرحمن الرحيم",
        "surah": "الفاتحة",
        "number": "1:1",
        "meaning": "أول آية في القرآن الكريم"
    },
    {
        "verse": "الحمد لله رب العالمين",
        "surah": "الفاتحة",
        "number": "1:2",
        "meaning": "حمد الله على نعمه"
    },
    {
        "verse": "إن الله مع الصابرين",
        "surah": "البقرة",
        "number": "2:153",
        "meaning": "الله ينصر الصابرين"
    },
    {
        "verse": "ولا تيأسوا من روح الله",
        "surah": "يوسف",
        "number": "12:87",
        "meaning": "عدم الاستسلام لليأس"
    },
    {
        "verse": "قل يا أيها الناس إني رسول الله إليكم جميعا",
        "surah": "الأعراف",
        "number": "7:158",
        "meaning": "رسالة النبي للجميع"
    },
]

def send_daily_verse():
    """إرسال آية يومية"""
    try:
        from datetime import datetime
        day_number = datetime.now().day % len(QURAN_VERSES)
        verse = QURAN_VERSES[day_number]
        
        message = f"""
🕌 *آية اليوم*

📖 *{verse['verse']}*

📚 *السورة:* {verse['surah']}
📍 *رقم الآية:* {verse['number']}
✨ *المعنى:* {verse['meaning']}

وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ ورَسُولُهُ والْمُؤْمِنُونَ
        """
        
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        logger.info(f"✅ تم إرسال الآية: {verse['number']}")
        
    except TelegramError as e:
        logger.error(f"❌ خطأ في الإرسال: {e}")
    except Exception as e:
        logger.error(f"❌ خطأ عام: {e}")

def schedule_daily_message():
    """جدولة الرسالة اليومية"""
    # تحديد الوقت (الساعة 8 صباحا)
    schedule.every().day.at("08:00").do(send_daily_verse)
    
    logger.info("⏰ تم جدولة الرسائل اليومية الساعة 8 صباحا")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logger.info("🤖 البوت يعمل الآن...")
    logger.info(f"⏰ سيتم إرسال آية كل يوم الساعة 8 صباحا")
    
    # تشغيل الجدولة في خيط منفصل
    scheduler_thread = threading.Thread(target=schedule_daily_message, daemon=True)
    scheduler_thread.start()
    
    # الاحتفاظ بالبرنامج يعمل
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت")pip install python-telegram-bot requests scheduleimport requests
import schedule
import time
from telegram import Bot
from telegram.error import TelegramError
import logging

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN)

def get_random_quran_verse():
    """جلب آية عشوائية من API القرآن"""
    try:
        response = requests.get("http://api.alquran.cloud/v1/randomaya")
        if response.status_code == 200:
            data = response.json()
            ayah = data['data']
            return {
                "text": ayah['text'],
                "surah": ayah['surah']['name'],
                "number": ayah['numberInSurah']
            }
    except Exception as e:
        logger.error(f"خطأ في API: {e}")
    return None

def send_daily_verse():
    """إرسال آية يومية"""
    verse = get_random_quran_verse()
    
    if verse:
        message = f"""
🕌 *آية اليوم*

📖 *{verse['text']}*

📚 *السورة:* {verse['surah']}
📍 *رقم الآية:* {verse['number']}
        """
        try:
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
            logger.info("✅ تم إرسال الآية")
        except TelegramError as e:
            logger.error(f"❌ خطأ: {e}")

def schedule_messages():
    schedule.every().day.at("08:00").do(send_daily_verse)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logger.info("🤖 البوت يعمل...")
    schedule_messages()import logging
from telegram import Bot
from telegram.error import TelegramError
import schedule
import time
from datetime import datetime
import requests
import threading

# ضع Token بوتك هنا
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"  # معرف القناة أو الجروب

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)

# قائمة بآيات قرآنية
QURAN_VERSES = [
    {
        "verse": "بسم الله الرحمن الرحيم",
        "surah": "الفاتحة",
        "number": "1:1",
        "meaning": "أول آية في القرآن الكريم"
    },
    {
        "verse": "الحمد لله رب العالمين",
        "surah": "الفاتحة",
        "number": "1:2",
        "meaning": "حمد الله على نعمه"
    },
    {
        "verse": "إن الله مع الصابرين",
        "surah": "البقرة",
        "number": "2:153",
        "meaning": "الله ينصر الصابرين"
    },
    {
        "verse": "ولا تيأسوا من روح الله",
        "surah": "يوسف",
        "number": "12:87",
        "meaning": "عدم الاستسلام لليأس"
    },
    {
        "verse": "قل يا أيها الناس إني رسول الله إليكم جميعا",
        "surah": "الأعراف",
        "number": "7:158",
        "meaning": "رسالة النبي للجميع"
    },
]

def send_daily_verse():
    """إرسال آية يومية"""
    try:
        from datetime import datetime
        day_number = datetime.now().day % len(QURAN_VERSES)
        verse = QURAN_VERSES[day_number]
        
        message = f"""
🕌 *آية اليوم*

📖 *{verse['verse']}*

📚 *السورة:* {verse['surah']}
📍 *رقم الآية:* {verse['number']}
✨ *المعنى:* {verse['meaning']}

وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ ورَسُولُهُ والْمُؤْمِنُونَ
        """
        
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        logger.info(f"✅ تم إرسال الآية: {verse['number']}")
        
    except TelegramError as e:
        logger.error(f"❌ خطأ في الإرسال: {e}")
    except Exception as e:
        logger.error(f"❌ خطأ عام: {e}")

def schedule_daily_message():
    """جدولة الرسالة اليومية"""
    # تحديد الوقت (الساعة 8 صباحا)
    schedule.every().day.at("08:00").do(send_daily_verse)
    
    logger.info("⏰ تم جدولة الرسائل اليومية الساعة 8 صباحا")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logger.info("🤖 البوت يعمل الآن...")
    logger.info(f"⏰ سيتم إرسال آية كل يوم الساعة 8 صباحا")
    
    # تشغيل الجدولة في خيط منفصل
    scheduler_thread = threading.Thread(target=schedule_daily_message, daemon=True)
    scheduler_thread.start()
    
    # الاحتفاظ بالبرنامج يعمل
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت")نشاء البوتات الرسمي).
**المحتوىح أن البوت سيرسل آية كل يوم الساعة 8 scheduler_thread = threading.Thread(target=schedule_daily_message,الة حمراء: "Sorry, this isn't a proper daemon=True)
scheduler_thread.start()

try:
    while True:
        time.sleep(1 name for a bot"
 - يعني أن اسم البو)
except KeyboardInterrupt:
    logger.info("تم إيقاف البوت")
```ت غير صحيح أو غير مقبول

**المشك

**الرد من المستخدم:**
"Sorry, this isnلة:**
- اسم البوت قد يكون يحتوي على أ't a proper name for a bot."

**المشكحرف غير مسموحة أو طول غلة:**
- اسم البوت ليس صحيحاً أو غير صحيح
- BotFather يطلب اسم صحيح للير مقبول من BotFather
- قد يكون الاسم يبوت

**الحل:**
- اختر اسم بوت جديحتوي على أحرف غير مسموحة أو كلمات محظورةد يتبع قواعد التسمية (أح

**الحل:**
- اختر اسم بورف وأرقام فقط،ت جديد وبسيط
- استخدم أحرف إنجليزية وأرقام وشرطات سفلية فقط
- مثال بدون علامات خاصة)
- مثال: `AlMuwnis_QuranBot` أو `QuranDailyBot`

هل تريد أن أساعدك في إنشاء بوت جديد باسم ص: `AlMuwnis_Quran_حيح؟import logging
from telegram import Bot
from telegram.error import TelegramError
import schedule
import time
from datetime import datetime
import requests
import threading

# ضع Token بوتك هنا
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"  # معرف القناة أو الجروب

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)

# قائمة بآيات قرآنية
QURAN_VERSES = [
    {
        "verse": "بسم الله الرحمن الرحيم",
        "surah": "الفاتحة",
        "number": "1:1",
        "meaning": "أول آية في القرآن الكريم"
    },
    {
        "verse": "الحمد لله رب العالمين",
        "surah": "الفاتحة",
        "number": "1:2",
        "meaning": "حمد الله على نعمه"
    },
    {
        "verse": "إن الله مع الصابرين",
        "surah": "البقرة",
        "number": "2:153",
        "meaning": "الله ينصر الصابرين"
    },
    {
        "verse": "ولا تيأسوا من روح الله",
        "surah": "يوسف",
        "number": "12:87",
        "meaning": "عدم الاستسلام لليأس"
    },
    {
        "verse": "قل يا أيها الناس إني رسول الله إليكم جميعا",
        "surah": "الأعراف",
        "number": "7:158",
        "meaning": "رسالة النبي للجميع"
    },
]

def send_daily_verse():
    """إرسال آية يومية"""
    try:
        from datetime import datetime
        day_number = datetime.now().day % len(QURAN_VERSES)
        verse = QURAN_VERSES[day_number]
        
        message = f"""
🕌 *آية اليوم*

📖 *{verse['verse']}*

📚 *السورة:* {verse['surah']}
📍 *رقم الآية:* {verse['number']}
✨ *المعنى:* {verse['meaning']}

وَقُلِ اعْمَلُوا فَسَيَرَى اللَّهُ عَمَلَكُمْ ورَسُولُهُ والْمُؤْمِنُونَ
        """
        
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        logger.info(f"✅ تم إرسال الآية: {verse['number']}")
        
    except TelegramError as e:
        logger.error(f"❌ خطأ في الإرسال: {e}")
    except Exception as e:
        logger.error(f"❌ خطأ عام: {e}")

def schedule_daily_message():
    """جدولة الرسالة اليومية"""
    # تحديد الوقت (الساعة 8 صباحا)
    schedule.every().day.at("08:00").do(send_daily_verse)
    
    logger.info("⏰ تم جدولة الرسائل اليومية الساعة 8 صباحا")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logger.info("🤖 البوت يعمل الآن...")
    logger.info(f"⏰ سيتم إرسال آية كل يوم الساعة 8 صباحا")
    
    # تشغيل الجدولة في خيط منفصل
    scheduler_thread = threading.Thread(target=schedule_daily_message, daemon=True)
    scheduler_thread.start()
    
    # الاحتفاظ بالبرنامج يعمل
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت")Alright, a new bot. How are we going to call it? Please choose a name for your bot.# AlMuwnis Quran Bot

بوت تيليجرام يومي يرسل آيات من المصحف في الصباح والمساء.

## المميزات
- إرسال آية يومية كل يوم الساعة 08:00 صباحاً
- إرسال آية يومية كل يوم الساعة 18:00 مساءً
- أوامر أساسية: `/start` و `/ayah` و `/help`
- يعتمد على API الرسمي للقرآن

## المتطلبات
- Python 3.10 أو أعلى
- حساب تيليجرام
- إنشاء بوت عبر @BotFather
- معرفة Chat ID للقناة أو الجروب

## التثبيت

1. انسخ ملف `.env.example` إلى `.env`
2. عدّل القيم:
   - `BOT_TOKEN=token_البوت`
   - `TARGET_CHAT_ID=chat_id_القناة_أو_الجروب`
3. ثبّت الحزم:

```bash
pip install -r requirements.txt
```

4. شغّل البوت:

```bash
python bot.py
```

## الحصول على Chat ID
- أضف البوت إلى القناة أو الجروب
- أرسل رسالة
- استخدم أحد البوتات التالية:
  - `@RawDataBot`
  - `@userinfobot`
- انسخ قيمة `chat id`

## ملاحظة
لا تنشر الـ Token في المستودع أو في القنوات العامة. استخدم ملف `.env` فقط.
