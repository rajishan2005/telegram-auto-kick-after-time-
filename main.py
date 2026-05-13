from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler
import asyncio

BOT_TOKEN = "8952613119:AAH18318ilnpQgxJ_1qQtUGg0d6qHokx_t0"
CHANNEL_ID = -1003806202683

async def joined(update: Update, context):
    user = update.chat_join_request.from_user

    print(f"{user.username} joined")

    # Approve join request
    await context.bot.approve_chat_join_request(
        chat_id=CHANNEL_ID,
        user_id=user.id
    )

    # Allow 60 seconds access
    await asyncio.sleep(60)

    # Permanently ban user
    await context.bot.ban_chat_member(
        chat_id=CHANNEL_ID,
        user_id=user.id
    )

    print(f"{user.username} permanently removed")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(ChatJoinRequestHandler(joined))

print("Bot running...")
app.run_polling()
