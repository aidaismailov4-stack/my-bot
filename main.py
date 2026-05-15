import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_KEY")

def get_ai_reply(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": text}]}]}
    try:
        response = requests.post(url, json=payload, timeout=20)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Бот загружается, подождите минуту..."

async def handle_msg(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.message.text:
        await u.message.reply_text(get_ai_reply(u.message.text))

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_msg))
    app.run_polling()
  
