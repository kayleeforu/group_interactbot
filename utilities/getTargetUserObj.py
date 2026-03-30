from utilities import userClass
from telegram import Update
from telegram.ext import ContextTypes
import db

database = db.Database()

async def getTargetUserObj(update: Update, context: ContextTypes.DEFAULT_TYPE, message, chatID):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        return userClass(user.id, chatID, user.first_name, user.username)

    if message.entities:
        for entity in message.entities:
            if entity.type == "text_mention":
                user = entity.user
                return userClass(user.id, chatID, user.first_name, user.username)

            elif entity.type == "mention":
                raw_username = message.text[entity.offset:entity.offset + entity.length]
                clean_username = raw_username.lstrip("@")
                
                db_user = database.getUserByUsername(clean_username, chatID)
                if db_user:
                    return userClass(db_user['userID'], chatID, db_user['firstname'], db_user['username'])
                
                try:
                    await context.bot.send_message(
                        chat_id = chatID,
                        text = "I am unable to find the user, please reply to their message with the command\n" \
                        "Or ask them to type something in chat and then /command @username."
                    )
                    return "Replied"
                except Exception as e:
                    print(f"Didn't find {raw_username}: {e}")
                    return None
                    
    return None