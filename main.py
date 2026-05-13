from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    CommandHandler,
    ContextTypes
)

import asyncio

BOT_TOKEN = "8952613119:AAH18318ilnpQgxJ_1qQtUGg0d6qHokx_t0"
CHANNEL_ID = -1003806202683

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Bot is running perfectly.")

# Join request handler
async def joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user

    print(f"{user.username} joined")

    # Approve join request
    await context.bot.approve_chat_join_request(
        chat_id=CHANNEL_ID,
        user_id=user.id
    )

    # Allow access for 60 seconds
    await asyncio.sleep(60)

    # Permanently ban user
    await context.bot.ban_chat_member(
        chat_id=CHANNEL_ID,
        user_id=user.id
    )

    print(f"{user.username} permanently removed")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(ChatJoinRequestHandler(joined))

print("Bot running...")

app.run_polling()
