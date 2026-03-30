from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db
from datetime import datetime, timezone
from random import randint

database = db.Database()


class User:
    def __init__(self, userID, chatID, firstname=None):
        self.id = int(userID)
        self.chatID = int(chatID)

        data = database.getUser(self.id, self.chatID)

        if data is None:
            database.insertNewUser(self.id, self.chatID, firstname or "Unknown")
            data = database.getUser(self.id, self.chatID)

        if firstname and data.get("firstname") != firstname:
            database.updateUserFirstname(self.id, self.chatID, firstname)
            data["firstname"] = firstname

        self.firstname = data.get("firstname")
        self.marriedTo = data.get("marriedTo")
        self.marriedAt = data.get("marriedAt")
        self.petID = data.get("petID")

    def updateUser(self, firstname=None, marriedTo=None, marriedAt=None, petID=None):
        if firstname is not None:
            database.updateUserFirstname(self.id, self.chatID, firstname)

        if marriedTo is not None:
            database.updateUserMarriedTo(self.id, self.chatID, marriedTo)

        if marriedAt is not None:
            database.updateUserMarriedAt(self.id, self.chatID, marriedAt)

        if petID is not None:
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
    proposingUserObj = User(proposingUser.id, chatID, proposingUser.first_name)

    if proposingUserObj.marriedTo is not None:
        marriedToObj = User(proposingUserObj.marriedTo, chatID)
        await context.bot.send_message(
            chat_id=chatID,
            text=f'<a href="tg://user?id={proposingUserObj.id}">{proposingUserObj.firstname}</a>, you are already married to <a href="tg://user?id={marriedToObj.id}">{marriedToObj.firstname}</a>!',
            parse_mode="HTML"
        )
        return

    message = update.effective_message

    proposingToUserObj = await getProposingToUserObj(update, context, message, chatID)

    if proposingToUserObj is None:
        await context.bot.send_message(
            chat_id=chatID,
            text="Please specify a user! (/marry @username or reply to someone)"
        )
        return

    if proposingUserObj.id == proposingToUserObj.id:
        await context.bot.send_message(
            chat_id=chatID,
            text="You can't marry yourself"
        )
        return

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
            InlineKeyboardButton("💍 Yes", callback_data=f"proposalYes:{chatID}:{proposingUserObj.id}:{proposingToUserObj.id}"),
            InlineKeyboardButton("💔 No", callback_data=f"proposalNo:{chatID}:{proposingUserObj.id}:{proposingToUserObj.id}")
        ]
    ])

    await context.bot.send_message(
        chat_id=chatID,
        text=f'<a href="tg://user?id={proposingUserObj.id}">{proposingUserObj.firstname}</a> is proposing to <a href="tg://user?id={proposingToUserObj.id}">{proposingToUserObj.firstname}</a>\nDo you accept this proposal?',
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
            show_alert=True
        )
        return

    if action == "proposalYes":
        await query.answer()

        time = datetime.now(timezone.utc).isoformat()

        proposingUserObj.updateUser(
            marriedTo=int(proposingToUserObj.id),
            marriedAt=time
        )
        proposingToUserObj.updateUser(
            marriedTo=int(proposingUserObj.id),
            marriedAt=time
        )

        text = f'<a href="tg://user?id={proposingUserObj.id}">{proposingUserObj.firstname}</a> and <a href="tg://user?id={proposingToUserObj.id}">{proposingToUserObj.firstname}</a> are now married! Let\'s congratulate them!'

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎊🎉", callback_data="nothing")]
        ])

        await query.edit_message_reply_markup(reply_markup=keyboard)

        choosePhoto = randint(1, 5)
        with open(f"resource/marriage/marriedCouple{choosePhoto}.jpg", "rb") as photo:
            await context.bot.send_photo(
                chat_id=chatID,
                caption=text,
                photo=photo,
                parse_mode="HTML"
            )

    elif action == "proposalNo":
        await query.answer()

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💔", callback_data="nothing")]
        ])

        await query.edit_message_text(
            text="The proposal was declined 💔",
            reply_markup=keyboard
        )


async def getProposingToUserObj(update: Update, context: ContextTypes.DEFAULT_TYPE, message, chatID):
    if message.reply_to_message:
        proposingToUser = message.reply_to_message.from_user
        return User(proposingToUser.id, chatID, proposingToUser.first_name)

    if message.entities:
        for entity in message.entities:
            if entity.type == "text_mention":
                proposingToUser = entity.user
                return User(proposingToUser.id, chatID, proposingToUser.first_name)

            elif entity.type == "mention":
                username = message.parse_entity(entity).lstrip("@")
                try:
                    proposingToUser = await context.bot.get_chat(username)
                    return User(proposingToUser.id, chatID, proposingToUser.first_name)
                except:
                    return None

    return None