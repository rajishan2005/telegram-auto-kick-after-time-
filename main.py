from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import asyncio

BOT_TOKEN = "8952613119:AAH18318ilnpQgxJ_1qQtUGg0d6qHokx_t0"
GROUP_ID = -1003544800297

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Preview bot is online and working."
    )

# New member join handler
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.new_chat_members:

        for user in update.message.new_chat_members:

            # Welcome message IN GROUP
            await context.bot.send_message(
                chat_id=GROUP_ID,
                text=(
                    f"Welcome {user.first_name}!\n\n"
                    f"You have 40 seconds to view the preview.\n"
                    f"After that, you will be removed automatically."
                )
            )

            print(f"{user.first_name} joined")

            # Wait 40 sec
            await asyncio.sleep(40)

            # Ban user
            await context.bot.ban_chat_member(
                chat_id=GROUP_ID,
                user_id=user.id
            )

            print(f"{user.first_name} removed")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome
    )
)

print("Bot running...")

app.run_polling()
