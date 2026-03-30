from telegram import Update
from telegram.ext import ContextTypes

async def processMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    isGroupChat = update.effective_chat.type in ["group", "supergroup"]
    if not isGroupChat:
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Sorry, currently I only work in group chats."
        )
        return