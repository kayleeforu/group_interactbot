from telegram import Update
from telegram.ext import ContextTypes
import db

database = db.Database()

async def processMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatID = update.effective_chat.id

    user = update.effective_user
    if not database.lookUpUser(user.id, chatID):
        database.insertNewUser(user.id, chatID, user.first_name)

    isGroupChat = update.effective_chat.type in ["group", "supergroup"]
    if not isGroupChat:
        await context.bot.send_message(
            chat_id = chatID,
            text = "Sorry, currently I only work in group chats."
        )
        return
    
    message = update.effective_message.text
    if message == "test":
        await context.bot.send_message(
            chat_id = chatID,
            text = "Hiii, <b>testing</b> things.",
            parse_mode = "HTML"
        )