import os
import requests
from telethon import TelegramClient, events

# بيانات التليجرام الخاصة بك
API_ID = int(os.environ.get("API_ID", "30188865"))
API_HASH = os.environ.get("API_HASH", "173663c51505ff2b5cb920d96afeeef4")

# بيانات البوت والقناة الناشرة
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8746024540:AAGy8Fr4YN-MEurYXsXlSBEJVNmmw8Rq0-A")
DESTINATION_CHAT = os.environ.get("DESTINATION_CHAT",320642604 )

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
    text_lower = text.lower()
    asset = "الأسواق العامة"
    if any(w in text_lower for w in ['gold', 'xau', 'ذهب', 'الذهب']):
        asset = "الذهب (XAUUSD)"
    elif any(w in text_lower for w in ['fed', 'dollar', 'usd', 'تضخم', 'فائدة', 'دولار']):
        asset = "الدولار الأمريكي (USD)"
    elif any(w in text_lower for w in ['oil', 'brent', 'نفط', 'النفط']):
        asset = "النفط (USOIL)"

    bullish_words = ['increase', 'rise', 'higher', 'growth', 'up', 'bullish', 'ارتفاع', 'نمو', 'إيجابي']
    bearish_words = ['decrease', 'fall', 'lower', 'drop', 'down', 'bearish', 'انخفاض', 'تراجع', 'سلبي']

    bull_score = sum(1 for word in bullish_words if word in text_lower)
    bear_score = sum(1 for word in bearish_words if word in text_lower)

    if bull_score > bear_score:
        sentiment = "📈 إيجابي (صاعد)"
        action = "شراء (BUY)"
        validity = "✅ خبر مؤكد وله تأثير إيجابي مباشر"
    elif bear_score > bull_score:
        sentiment = "📉 سلبي (هابط)"
        action = "بيع (SELL)"
        validity = "✅ خبر مؤكد وله تأثير سلبي مباشر"
    else:
        sentiment = "⚠️ محايد / غير حاسم"
        action = "مراقبة الانتظار (WAIT)"
        validity = "ℹ️ خبر إخباري عام"

    return {"asset": asset, "sentiment": sentiment, "action": action, "validity": validity}

@client.on(events.NewMessage(chats=MONITORED_CHANNELS))
async def handle_new_message(event):
    raw_text = event.raw_text
    analysis = analyze_news_ai(raw_text)

    formatted_signal = (
        f"🚨 *إشارة خبر عاجل (Omar Forex Bot)* 🚨\n\n"
        f"📰 *الخبر:* \n`{raw_text}`\n\n"
        f"-----------------------------------\n"
        f"🔍 *التقييم:* {analysis['validity']}\n"
        f"🎯 *الأصل المتأثر:* {analysis['asset']}\n"
        f"📊 *الاتجاه:* {analysis['sentiment']}\n"
        f"💡 *التوصية:* *{analysis['action']}*\n"
        f"-----------------------------------\n"
        f"🤖 _تم النشر بواسطة @OmarForexNews_bot_"
    )
    send_via_bot(formatted_signal)

async def main():
    print("🚀 البوت شغال على Railway ويراقب الأخبار 24/7...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
