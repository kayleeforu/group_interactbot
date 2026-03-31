from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from utilities.User import User
from utilities.Pet import Pet
import db

database = db.Database()
WAITING_FOR_NAME = 1

async def getPet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatID = update.effective_chat.id
    user = User(update.effective_user.id, chatID)
    if user.petID is not None:
        await context.bot.send_message(
            chat_id=chatID,
            text="Sorry, but you already have a pet."
        )
        return ConversationHandler.END
    
    await context.bot.send_message(
        chat_id=chatID,
        text="Write the name for your pet!"
    )
    return WAITING_FOR_NAME

async def gotName(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatID = update.effective_chat.id
    name = update.effective_message.text
    if len(name) > 24:
        await context.bot.send_message(
            chat_id=chatID,
            text="The name is too long. Max 24 symbols."
        )
        return WAITING_FOR_NAME

    userObj = User(update.effective_user.id, chatID)

    typeKeyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🐈 Cat", callback_data=f"{userObj.id}:{chatID}:cat:{name}"),
            InlineKeyboardButton("🐩 Dog", callback_data=f"{userObj.id}:{chatID}:dog:{name}"),
            InlineKeyboardButton("🐷 Pig", callback_data=f"{userObj.id}:{chatID}:pig:{name}"),
            InlineKeyboardButton("🐇 Bunny", callback_data=f"{userObj.id}:{chatID}:bunny:{name}"),
            InlineKeyboardButton("🐥 Chicken", callback_data=f"{userObj.id}:{chatID}:chicken:{name}")
        ]
    ])
    await context.bot.send_message(
        chat_id=chatID,
        text="Choose your pet type!",
        reply_markup=typeKeyboard,
    )
    return ConversationHandler.END

async def petType_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    data = query.data.split(":")
    if len(data) != 4:
        await query.answer("You can't use ':' in the pet's name!", show_alert=True)
        return

    userID, chatID, petType, petName = data

    if query.from_user.id != int(userID):
        await query.answer("This is not your pet!", show_alert=True)
        return

    await query.answer()

    pet = Pet(int(userID), petName, petType, False)
    database.updateUserPet(int(userID), int(chatID), pet.petID)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎊🎉", callback_data="nothing")]
    ])
    await query.edit_message_text(
        text=f"Congratulations! You adopted a new pet.\nIts name is {pet.petName} the {pet.petType}!",
        reply_markup=keyboard
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled!")
    return ConversationHandler.END