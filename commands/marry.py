from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db
from datetime import datetime, timezone

database = db.Database()

class User:
    def __init__(self, userID, chatID):
        self.id = userID
        self.chatID = chatID
        self.firstname = database.getFirstname(self.id, self.chatID)
        self.marriedTo = database.getUserMarriedTo(self.id, self.chatID)
        self.marriedAt = database.getUserMarriedAt(self.id, self.chatID)
        self.petID = database.getPet(self.id, self.chatID)
    
    def updateUser(self, firstname=None, marriedTo=None, marriedAt=None, petID=None):
        infoToUpdate = {
            "firstname": firstname,
            "marriedTo": marriedTo,
            "marriedAt": marriedAt,
            "petID": petID
        }
        for entry in infoToUpdate:
            if entry == "firstname" and infoToUpdate["firstname"] is not None:
                database.updateUserFirstname(self.id, self.chatID, firstname)
            elif entry == "marriedTo" and infoToUpdate["marriedTo"] is not None:
                database.updateUserMarriedTo(self.id, self.chatID, marriedTo)
            elif entry == "marriedAt" and infoToUpdate["marriedAt"] is not None:
                database.updateUserMarriedAt(self.id, self.chatID, marriedAt)
            elif entry == "petID" and infoToUpdate["petID"] is not None:
                database.updateUserPet(self.id, self.chatID, petID)

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
    if not database.lookUpUser(proposingUser.id, chatID):
        database.insertNewUser(proposingUser.id, chatID, proposingUser.first_name)

    proposingUserObj = User(proposingUser.id, chatID)

    if proposingUserObj.marriedTo is not None:
        marriedToObj = User(proposingUserObj.marriedTo, chatID)
        await context.bot.send_message(
            chat_id=chatID,
            text=f'<a href="tg://user?id={proposingUserObj.id}">{proposingUserObj.firstname}</a>, you are already married to <a href="tg://user?id={marriedToObj.id}">{marriedToObj.firstname}</a>!',
            parse_mode="HTML"
        )
        return

    message = update.effective_message
    proposingToUser = None
    for entry in message.entities:
        if entry.type == "mention":
            proposingToUsername = message.parse_entity(entry)
            proposingToUser = await context.bot.get_chat(proposingToUsername)
            if not database.lookUpUser(proposingToUser.id, chatID):
                database.insertNewUser(proposingToUser.id, chatID, proposingToUser.first_name)
            break
        elif entry.type == "text_mention":
            proposingToUser = entry.user
            if not database.lookUpUser(proposingToUser.id, chatID):
                database.insertNewUser(proposingToUser.id, chatID, proposingToUser.first_name)
            break

    if proposingToUser is None:
        await context.bot.send_message(
            chat_id=chatID,
            text="Please specify a user! Example: /marry @username"
        )
        return

    proposingToUserObj = User(proposingToUser.id, chatID)

    if proposingToUserObj.marriedTo is not None:
        marriedToObj = User(proposingToUserObj.marriedTo, chatID)
        await context.bot.send_message(
            chat_id=chatID,
            text=f'<a href="tg://user?id={proposingToUserObj.id}">{proposingToUserObj.firstname}</a> is already married to <a href="tg://user?id={marriedToObj.id}">{marriedToObj.firstname}</a>!',
            parse_mode="HTML"
        )
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💍Yes", callback_data=f"proposalYes:{chatID}:{proposingUserObj.id}:{proposingToUserObj.id}"),
            InlineKeyboardButton("💔No", callback_data=f"proposalNo:{chatID}:{proposingUserObj.id}:{proposingToUserObj.id}")
        ]
    ])

    await context.bot.send_message(
        chat_id=chatID,
        text=f'<a href="tg://user?id={proposingUserObj.id}">{proposingUserObj.firstname}</a> is proposing to <a href="tg://user?id={proposingToUserObj.id}">{proposingToUserObj.firstname}</a>\nWhat are they going to say?',
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def marry_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "nothing":
        await query.answer()
        return

    action, chatID, proposingUserID, proposingToUserID = query.data.split(":")
    chatID = int(chatID)

    proposingUserObj = User(proposingUserID, chatID)
    proposingToUserObj = User(proposingToUserID, chatID)

    if query.from_user.id != int(proposingToUserObj.id):
        await query.answer(
            text="This proposal is not for you!",
            show_alert=True)
    elif query.from_user.id == int(proposingToUserObj.id):
        if action == "proposalYes":
            await query.answer()

            time = datetime.now(timezone.utc).isoformat()
            proposingUserObj.updateUser(marriedTo=int(proposingToUserObj.id), marriedAt=time)
            proposingToUserObj.updateUser(marriedTo=int(proposingUserObj.id), marriedAt=time)

            text = f'<a href="tg://user?id={proposingUserObj.id}">{proposingUserObj.firstname}</a> and <a href="tg://user?id={proposingToUserObj.id}">{proposingToUserObj.firstname}</a> are now married! Let\'s congratulate them!'

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🎊🎉", callback_data="nothing")
                ]
            ])

            await query.edit_message_reply_markup(reply_markup=keyboard)

            await context.bot.send_photo(
                chat_id=chatID,
                caption=text,
                photo=open("resource/marriage/marriedCoupleOne.jpg", "rb"),
                parse_mode="HTML"
            )

        elif action == "proposalNo":
            await query.answer()

            text = "The proposal was declined 💔"

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("💔", callback_data="nothing")
                ]
            ])

            await query.edit_message_text(text=text, reply_markup=keyboard)