from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from random import random
from utilities.User import User
from utilities.Pet import Pet
import db
from time import sleep

WAITING_FOR_NAME = 1

async def getPet(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    user = User(update.effective_user.id, update.effective_chat.id)
    if user.petID is not None:
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Sorry, but you already have a pet"
        )
        return ConversationHandler.END
    
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Write the name for your pet in this chat"
    )
    return WAITING_FOR_NAME

async def gotName(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_message.text

    if len(name) > 24:
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "The name is too long. Max 24 symbols."
        )
        return WAITING_FOR_NAME
    
    userObj = User(update.effective_user.id, update.effective_chat.id)
    
    typeKeyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🐈 Cat", callback_data = f"{userObj.id}:cat:{name}"),
            InlineKeyboardButton("🐩 Dog", callback_data = f"{userObj.id}:dog:{name}"),
            InlineKeyboardButton("🐷 Pig", callback_data = f"{userObj.id}:pig:{name}"),
            InlineKeyboardButton("🐇 Bunny", callback_data = f"{userObj.id}:bunny:{name}"),
            InlineKeyboardButton("🐥 Chicken", callback_data = f"{userObj.id}:chicken:{name}")
        ]
    ])
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Choose your pet",
        reply_markup = typeKeyboard,
    )

    return ConversationHandler.END

async def petType_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "nothing":
        await query.answer()
        return
    
    data = update.callback_query.data.split(":")

    if len(data) > 3:
        await query.edit_message_text(
            text = f"You can't use ':' in pet's name",
        )
        return

    userID, petType, petName = data

    pet = Pet(userID, petName, petType, False)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎊🎉", callback_data="nothing")
        ]
    ])

    await query.edit_message_text(
        text = f"Congratulate you adopted your new pet.\nIts name is {pet.petName}",
        reply_markup = keyboard
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END