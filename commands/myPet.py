from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utilities.User import User
from utilities.Pet import Pet

async def myPet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatID = update.effective_chat.id
    isGroupChat = update.effective_chat.type in ["group", "supergroup"]

    if not isGroupChat:
        await context.bot.send_message(
            chat_id=chatID,
            text="Sorry, currently I only work in group chats."
        )
        return
    
    user = User(update.effective_user.id, chatID)
    pet = Pet(user.id)
    
    if pet.petID is None:
        await context.bot.send_message(
            chat_id = chatID,
            text = "Sorry, but you don't have a pet.\nGet one by typing /getpet."
        )
        return
    
    text = f'Here is the information about your pet {pet.petNaem}:\nAnimal: {pet.petType}\n'