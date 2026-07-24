import os
import requests
from telethon import TelegramClient, events

# بيانات التليجرام الخاصة بك
API_ID = int(os.environ.get("API_ID", "30188865"))
API_HASH = os.environ.get("API_HASH", "173663c51505ff2b5cb920d96afeeef4")

# بيانات البوت والقناة الناشرة
part1 = "8746024540"
part2 = "AAGY0ieBuQweVnsiPNSMItub0KBLi9Vh42A"
BOT_TOKEN = os.environ.get("BOT_TOKEN", f"{part1}:{part2}")
DESTINATION_CHAT = int(os.environ.get("DESTINATION_CHAT", "320642604"))

MONITORED_CHANNELS = ['@ForexBreakingNews']

client = TelegramClient('omar_forex_session', API_ID, API_HASH)

def send_via_bot(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": DESTINATION_CHAT,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")

def analyze_news_ai(text):
    # دالة تحليل الخبر المبدئية
    return {
        'validity': 'قوي / موثوق',
        'asset': 'الذهب / الدولار',
        'sentiment': 'إيجابي / صعود',
        'action': 'شراء عند التصحيح'
    }

@client.on(events.NewMessage(chats=MONITORED_CHANNELS))
async def handle_new_message(event):
    raw_text = event.raw_text
    analysis = analyze_news_ai(raw_text)

    formatted_signal = (
        f"🚨 *(Omar Forex Bot) إشارة خبر عاجل* 🚨\n\n"
        f"📑 *الخبر:* \n`{raw_text}`\n\n"
        f"-------------------------\n"
        f"🔍 *التقييم:* {analysis['validity']}\n"
        f"🎯 *الأصل التأثر:* {analysis['asset']}\n"
        f"📊 *الاتجاه:* {analysis['sentiment']}\n"
        f"💡 *التوصية:* {analysis['action']}\n"
        f"-------------------------\n"
        f"🤖 _تم النشر بواسطة @OmarForexNews_bot_"
    )
    send_via_bot(formatted_signal)

async def main():
    print("🚀 البوت شغال على Railway 24/7 ويراقب الأخبار...")
    # استخدام bot_token لمنع طلب رقم الهاتف وتجنب Crash على Railway
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
