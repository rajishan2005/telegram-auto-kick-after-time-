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
CHANNEL_ID = -1003544800297

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Preview bot is online and working."
    )

# Detect new members
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for user in update.message.new_chat_members:

        print(f"{user.first_name} joined")

        # DM user
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=(
                    f"Welcome {user.first_name}!\n\n"
                    f"You have 40 seconds to preview the content.\n"
                    f"After that, you will be removed automatically."
                )
            )
        except:
            print("Could not DM user")

        # Wait 40 seconds
        await asyncio.sleep(40)

        # Ban user permanently
        await context.bot.ban_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user.id
        )

        print(f"{user.first_name} removed")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        new_member
    )
)

print("Bot running...")

app.run_polling()
