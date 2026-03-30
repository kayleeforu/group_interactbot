from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utilities.User import User
import db
from datetime import datetime, timezone

database = db.Database()

def buildPairs(response, chatID):
    processed = {}
    pairs = []
    now = datetime.now(timezone.utc)
    for row in response:
        firstUserObj = User(int(row["userID"]), chatID)
        secondUserObj = User(int(row["marriedTo"]), chatID)
        if firstUserObj.id in processed or secondUserObj.id in processed:
            continue
        marriedAt = datetime.fromisoformat(row["marriedAt"])
        difference = now - marriedAt
        days = difference.days
        hours = difference.seconds // 3600
        minutes = (difference.seconds % 3600) // 60
        marriedFor = f"{days} days {hours} hours {minutes} minutes"
        pairs.append([firstUserObj, secondUserObj, marriedFor])
        processed[firstUserObj.id] = True
        processed[secondUserObj.id] = True
    return pairs

def buildText(pairs, page):
    start = page * 8
    end = start + 8
    slice = pairs[start:end]
    text = "The list of marriages in this chat:\n"
    for i, entry in enumerate(slice):
        count = start + i + 1
        text += f'{count}. <a href="tg://user?id={entry[0].id}">{entry[0].firstname}</a> and <a href="tg://user?id={entry[1].id}">{entry[1].firstname}</a>. Married for {entry[2]}.\n'
    return text

def buildKeyboard(pairs, page, chatID):
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"marriages_page:{chatID}:{page - 1}"))
    if (page + 1) * 8 < len(pairs):
        buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"marriages_page:{chatID}:{page + 1}"))
    if not buttons:
        return None
    return InlineKeyboardMarkup([buttons])

async def getMarriages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatID = update.effective_chat.id
    response = database.getMarriedList(chatID)

    if await responseEmpty(context, response, chatID):
        return

    pairs = buildPairs(response, chatID)
    text = buildText(pairs, 0)
    keyboard = buildKeyboard(pairs, 0, chatID)

    await context.bot.send_message(
        chat_id=chatID,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def marriages_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, chatID, page = query.data.split(":")
    chatID = int(chatID)
    page = int(page)

    response = database.getMarriedList(chatID)
    pairs = buildPairs(response, chatID)
    text = buildText(pairs, page)
    keyboard = buildKeyboard(pairs, page, chatID)

    await query.edit_message_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def responseEmpty(context, response, chatID):
    if response is None:
        await context.bot.send_message(
            chat_id=chatID,
            text="There are no marriages in this chat yet."
        )
        return True
    return False