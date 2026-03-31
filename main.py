import logging
from telegram.ext import ApplicationBuilder, filters, MessageHandler, CommandHandler, CallbackQueryHandler, ConversationHandler
import os
from handlers.messageHandler import processMessage
from commands.marry import marry, marry_callback
from commands.kissHug import kissHug
from functools import partial
from commands.marriages import getMarriages, marriages_callback
from commands.getPet import getPet, gotName, cancel, WAITING_FOR_NAME, petType_callback

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
    kissCommand = CommandHandler("kiss", kissHug)
    hugCommand = CommandHandler("hug", partial(kissHug, action="hug"))
    marriagesCommand = CommandHandler("marriages", getMarriages)

    
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler("getPet", getPet)],
        states = {
            WAITING_FOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, gotName)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        conversation_timeout = 60
    )
    application.add_handler(conv_handler)

    application.add_handler(kissCommand)
    application.add_handler(hugCommand)
    application.add_handler(marryCommand)
    application.add_handler(marriagesCommand)
    application.add_handler(CallbackQueryHandler(marry_callback, pattern=r"^proposal(Yes|No):"))
    application.add_handler(CallbackQueryHandler(marriages_callback, pattern=r"^marriages_page:"))
    application.add_handler(CallbackQueryHandler(petType_callback, pattern=r"^\d+:\-?\d+:(cat|dog|pig|bunny|chicken):"))
    application.add_handler(messageHandler)
    
    # Run bot
    application.run_polling()