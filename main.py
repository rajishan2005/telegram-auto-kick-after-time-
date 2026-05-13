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

# ---------------- START COMMAND ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Preview bot is online."
    )

# ---------------- NEW MEMBER ----------------

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    for user in update.message.new_chat_members:

        # Send welcome message
        msg = await update.message.reply_text(
            f"Welcome {user.first_name}!\n"
            f"You have 40 seconds to preview the content."
        )

        print(f"{user.first_name} joined")

        # Delete welcome message after 10 sec
        async def delete_message():
            await asyncio.sleep(10)

            try:
                await msg.delete()
            except:
                pass

        asyncio.create_task(delete_message())

        # Remove user after 40 sec
        async def remove_user(user_id, name):

            await asyncio.sleep(40)

            try:
                # Ban
                await context.bot.ban_chat_member(
                    chat_id=chat_id,
                    user_id=user_id
                )

                # Instantly unban so they can join again later
                await context.bot.unban_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    only_if_banned=True
                )

                print(f"{name} removed")

            except Exception as e:
                print(e)

        asyncio.create_task(
            remove_user(user.id, user.first_name)
        )

# ---------------- UNBAN COMMAND ----------------

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    if not context.args:
        await update.message.reply_text(
            "Usage: /unban USER_ID"
        )
        return

    try:
        user_id = int(context.args[0])

        await context.bot.unban_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )

        await update.message.reply_text(
            f"User {user_id} unbanned."
        )

    except:
        await update.message.reply_text(
            "Invalid user ID."
        )

# ---------------- MAIN ----------------

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("unban", unban))

app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        new_member
    )
)

print("Bot running...")

app.run_polling()
