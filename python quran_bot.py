import requests
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
    schedule_messages()