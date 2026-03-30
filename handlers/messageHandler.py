from telegram import Update
from telegram.ext import ContextTypes

async def processMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatID = update.effective_chat.id

    isGroupChat = update.effective_chat.type in ["group", "supergroup"]
    if not isGroupChat:
        context.bot.send_message(
            chat_id = chatID,
            text = "Sorry, currently I only work in group chats."
        )
        return
    
    message = update.effective_message.text
    if message == "test":
        context.bot.send_message(
            chat_id = chatID,
            text = "Hiii, <bold>testing</bold> things.",
            parse_mode = "HTML"
        )