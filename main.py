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
GROUP_ID = -1003806202683

# Store banned users
banned_users = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Preview bot is online and working."
    )

# Detect new members
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.new_chat_members:

        for user in update.message.new_chat_members:

            # Save user for unban command
            banned_users[user.username] = user.id

            # Send welcome message
            msg = await context.bot.send_message(
                chat_id=GROUP_ID,
                text=(
                    f"Welcome {user.first_name}!\n\n"
                    f"You have 40 seconds to view the preview.\n"
                    f"After that, you will be removed automatically."
                )
            )

            print(f"{user.first_name} joined")

            # Wait 10 sec
            await asyncio.sleep(10)

            # Delete welcome message
            await context.bot.delete_message(
                chat_id=GROUP_ID,
                message_id=msg.message_id
            )

            # Remaining 30 sec
            await asyncio.sleep(30)

            # Kick user
            await context.bot.ban_chat_member(
                chat_id=GROUP_ID,
                user_id=user.id
            )

            print(f"{user.first_name} removed")

# /unban command
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage: /unban username"
        )
        return

    username = context.args[0].replace("@", "")

    if username not in banned_users:
        await update.message.reply_text(
            "User not found."
        )
        return

    user_id = banned_users[username]

    await context.bot.unban_chat_member(
        chat_id=GROUP_ID,
        user_id=user_id
    )

    await update.message.reply_text(
        f"@{username} has been unbanned."
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("unban", unban))

app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome
    )
)

print("Bot running...")

app.run_polling()
