import logging
from telegram.ext import ApplicationBuilder, filters, MessageHandler, CommandHandler, CallbackQueryHandler
import os
from handlers.messageHandler import processMessage
from commands.marry import marry, marry_callback

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
    marryCommand = CommandHandler("marry", marry)
    
    application.add_handlers([messageHandler, marryCommand])
    application.add_handler(CallbackQueryHandler(marry_callback, pattern=r"^proposal(Yes|No):"))
    
    # Run bot
    application.run_polling()