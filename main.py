from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import asyncio

BOT_TOKEN = "YOUR_BOT_TOKEN"
GROUP_ID = -100XXXXXXXXXX

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Preview bot is online."
    )

# Detect joins
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.new_chat_members:

        for user in update.message.new_chat_members:

            await update.message.reply_text(
                f"Welcome {user.first_name}!\n\n"
                f"You have 40 seconds to view the preview."
            )

            print(f"{user.first_name} joined")

            await asyncio.sleep(40)

            await context.bot.ban_chat_member(
                chat_id=GROUP_ID,
                user_id=user.id
            )

            print(f"{user.first_name} removed")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome
    )
)

print("Bot running...")

app.run_polling()
