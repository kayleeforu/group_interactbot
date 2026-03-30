from telegram import Update
from telegram.ext import ContextTypes
from utilities.User import User
from random import randint
from utilities.getTargetUserObj import getTargetUserObj

async def kissHug(update: Update, context: ContextTypes.DEFAULT_TYPE, action = "kiss"):
    if invalidUser(update):
        return
    
    chatID = update.effective_chat.id
    user = update.effective_user

    message = update.effective_message

    calledUser = User(user.id, chatID, user.first_name, user.username)
    targetUser = await getTargetUserObj(update, context, message, chatID)
    if not targetUser or targetUser == "Replied":
        return

    if str(targetUser.id) == "592895797" and str(calledUser.id) != "977796454":
        await context.bot.send_message(
            chat_id = chatID,
            text = "No."
        )
        return

    chosenPhoto = randint(1, 5)
    with open (f"resource/{action}/{action}{chosenPhoto}.jpg", "rb") as photo:
        await context.bot.send_photo(
            chat_id = chatID,
            photo = photo,
            caption = f'<a href="tg://user?id={calledUser.id}">{calledUser.firstname}</a> {"kissed" if action == "kiss" else "hugged"} <a href="tg://user?id={targetUser.id}">{targetUser.firstname}</a>',
            parse_mode = "HTML"
        )

def invalidUser(update: Update):
    if not update.effective_user or update.effective_user.is_bot:
        return True
    return False