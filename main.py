import logging
from telegram.ext import ApplicationBuilder, filters, MessageHandler
import os
from handlers.messageHandler import processMessage

logging.basicConfig(
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   level=logging.INFO
)

if __name__ == '__main__':
    TOKEN = os.environ.get("INTERACTBOT_TOKEN")
    BOT_API_URL = os.getenv("BOT_API_URL", "http://telegram-bot-api:8081/bot")
    BOT_API_FILE_URL = os.getenv("BOT_API_FILE_URL", "http://telegram-bot-api:8081/file/bot")

    application = ApplicationBuilder() \
        .token(TOKEN) \
        .base_url(BOT_API_URL) \
        .base_file_url(BOT_API_FILE_URL) \
        .concurrent_updates(True) \
        .read_timeout(120) \
        .write_timeout(120) \
        .connect_timeout(120) \
        .build()

    # Message Handler
    messageHandler = MessageHandler(filters.TEXT, processMessage)
    
    application.add_handlers([messageHandler])
    
    # Run bot
    application.run_polling()