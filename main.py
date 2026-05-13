from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ChatJoinRequestHandler,
    ContextTypes
)

import asyncio

BOT_TOKEN = "8952613119:AAH18318ilnpQgxJ_1qQtUGg0d6qHokx_t0"
CHANNEL_ID = -1003806202683

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Preview bot is online and working."
    )

# User join handler
async def joined(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.chat_join_request.from_user

    print(f"{user.first_name} joined")

    # Approve join request
    await context.bot.approve_chat_join_request(
        chat_id=CHANNEL_ID,
        user_id=user.id
    )

    # DM user
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=(
                f"Hi {user.first_name}!\n\n"
                f"You now have 40 seconds to view the preview.\n"
                f"After that, access will be removed automatically."
            )
        )
    except:
        print("Could not DM user")

    # Wait 40 seconds
    await asyncio.sleep(40)

    # Kick/Ban user
    await context.bot.ban_chat_member(
        chat_id=CHANNEL_ID,
        user_id=user.id
    )

    print(f"{user.first_name} removed")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(ChatJoinRequestHandler(joined))

print("Bot running...")

app.run_polling()
