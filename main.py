import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Настройка логирования, чтобы видеть ошибки в Render
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Берем ключи из Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Настройка Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Сначала отправляем статус
    status_msg = await update.message.reply_text("Бот думает...")
    
    try:
        # Запрос к нейросети
        response = model.generate_content(user_text)
        await status_msg.edit_text(response.text)
    except Exception as e:
        # Если будет ошибка, ты увидишь её прямо в Telegram
        await status_msg.edit_text(f"Ошибка Gemini: {str(e)}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Бот успешно запущен!")
    application.run_polling()
    
