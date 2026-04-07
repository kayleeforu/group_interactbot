from telegram import Update
from telegram.ext import ContextTypes
import db
from commands.marry import User
import logging

database = db.Database()

async def processMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_sender.id) == "5631259670":
        await context.bot.delete_message(
            chat_id = update.effective_chat.id,
            message_id = update.effective_message.id
        )
    else:
        logging.info(f"user id: {update.effective_sender.id}, username: {update.effective_sender.first_name}")


    if not update.effective_user or update.effective_user.is_bot:
        return

    chatID = update.effective_chat.id
    user = update.effective_user

    User(user.id, chatID, user.first_name, user.username)

    isGroupChat = update.effective_chat.type in ["group", "supergroup"]
    if not isGroupChat:
        await context.bot.send_message(
            chat_id = chatID,
            text = "Sorry, currently I only work in group chats."
        )
        return
    
    if not update.effective_message.text:
        return

    message = update.effective_message.text
    if message == "test":
        await context.bot.send_message(
            chat_id = chatID,
            text = "Hiii, <b>testing</b> things.",
            parse_mode = "HTML"
        )