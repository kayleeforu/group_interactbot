from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db
from datetime import datetime, timezone

database = db.Database()

class User:
    def __init__(self, userID):
        self.id = userID
        self.firstname = database.getFirstname(self.id)
        self.marriedTo = database.getUserMarriedTo(self.id)
        self.marriedAt = database.getUserMarriedAt(self.id)
        self.petID = database.getPet(self.id)
    
    def updateUser(self, firstname=None, marriedTo=None, marriedAt = None, petID=None):
        infoToUpdate = {
            "firstname": firstname,
            "marriedTo": marriedTo,
            "marriedAt": marriedAt,
            "petID": petID
        }
        for entry in infoToUpdate:
            if entry == "firstname" and infoToUpdate["firstname"] is not None:
                database.updateUserFirstname(self.id, firstname)
            elif entry == "marriedTo" and infoToUpdate["marriedTo"] is not None:
                database.updateUserMarriedTo(self.id, marriedTo)
            elif entry == "marriedAt" and infoToUpdate["marriedAt"] is not None:
                database.updateUserMarriedAt(self.id, marriedAt)
            elif entry == "petID" and infoToUpdate["petID"] is not None:
                database.updateUserPet(self.id, petID)

async def marry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatID = update.effective_chat.id
    isGroupChat = update.effective_chat.type in ["group", "supergroup"]
    if not isGroupChat:
        await context.bot.send_message(
            chat_id=chatID,
            text="Sorry, currently I only work in group chats."
        )
        return

    proposingUser = update.effective_user
    if not database.lookUpUser(proposingUser.id):
        database.insertNewUser(proposingUser.id, proposingUser.first_name)

    proposingUserObj = User(proposingUser.id)

    # If user A is already married
    if proposingUserObj.marriedTo is not None:
        marriedToObj = User(proposingUserObj.marriedTo)
        await context.bot.send_message(
            chat_id=chatID,
            text=f'<a href="tg://user?id={proposingUserObj.id}">{proposingUserObj.firstname}</a>, you are already married to <a href="tg://user?id={marriedToObj.id}">{marriedToObj.firstname}</a>!',
            parse_mode="HTML"
        )
        return

    # Get who user A is proposing to (user B)
    message = update.effective_message
    proposingToUsername = None
    proposingToUser = None
    for entry in message.entities:
        if entry.type == "mention":
            proposingToUsername = message.parse_entity(entry)
            proposingToUser = await context.bot.get_chat(proposingToUsername)
            if not database.lookUpUser(proposingToUser.id):
                database.insertNewUser(proposingToUser.id, proposingToUser.first_name)
            break
        elif entry.type == "text_mention":
            proposingToUser = entry.user
            proposingToFirstname = proposingToUser.first_name
            proposingToID = proposingToUser.id
            if not database.lookUpUser(proposingToID):
                database.insertNewUser(proposingToID, proposingToFirstname)
            break

    if proposingToUser is None:
        await context.bot.send_message(
            chat_id=chatID,
            text="Please specify a user! Example: /marry @username"
        )
        return

    proposingToUserObj = User(proposingToUser.id)

    # If user B is already married
    if proposingToUserObj.marriedTo is not None:
        marriedToObj = User(proposingToUserObj.marriedTo)
        await context.bot.send_message(
            chat_id=chatID,
            text=f'<a href="tg://user?id={proposingToUserObj.id}">{proposingToUserObj.firstname}</a> is already married to <a href="tg://user?id={marriedToObj.id}">{marriedToObj.firstname}</a>!',
            parse_mode="HTML"
        )
        return
    
    # Both users aren't married, send a proposal to user B from user A
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💍Yes", callback_data = f"proposalYes:{proposingUserObj.id}:{proposingToUserObj.id}"),
            InlineKeyboardButton("💔No", callback_data = f"proposalNo:{proposingUserObj.id}:{proposingToUserObj.id}")
        ]
    ])

    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'<a href="tg://user?id={proposingUserObj.id}">{proposingUserObj.firstname}</a> is proposing to <a href="tg://user?id={proposingToUserObj.id}">{proposingToUserObj.firstname}</a>\nWhat are they going to say?',
        reply_markup = keyboard,
        parse_mode = "HTML"
    )

async def marry_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "nothing":
        await query.answer()
        return

    action, proposingUserID, proposingToUserID = query.data.split(":")

    proposingUserObj = User(proposingUserID)
    proposingToUserObj = User(proposingToUserID)

    if query.from_user.id != int(proposingToUserObj.id):
        await query.answer(
            text = "This proposal is not for you!",
            show_alert = True)
    elif query.from_user.id == int(proposingToUserObj.id):
        if action == "proposalYes":
            await query.answer()

            time = datetime.now(timezone.utc).isoformat()
            proposingUserObj.updateUser(marriedTo = int(proposingToUserObj.id), marriedAt = time)
            proposingToUserObj.updateUser(marriedTo = int(proposingUserObj.id), marriedAt = time)

            text = f'<a href="tg://user?id={proposingUserObj.id}">{proposingUserObj.firstname}</a> and <a href="tg://user?id={proposingToUserObj.id}">{proposingToUserObj.firstname}</a> are now married! Let\'s congratulate them!' 
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🎊🎉", callback_data = "nothing")
                ]
            ])

            await query.edit_message_reply_markup(reply_markup=keyboard)

            await context.bot.send_photo(
                chat_id = update.effective_chat.id,
                caption = text,
                photo = open("resource/marriage/marriedCoupleOne.jpg", "rb"),
                parse_mode = "HTML"
            )
        
        elif action == "proposalNo":
            await query.answer()

            text = "The proposal was declined 💔"
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("💔", callback_data = "nothing")
                ]
            ])

            await query.edit_message_text(text=text, reply_markup=keyboard)