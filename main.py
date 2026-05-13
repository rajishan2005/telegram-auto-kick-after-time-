from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler
import asyncio

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN"
CHANNEL_ID = -1001234567890

async def joined(update: Update, context):
    user = update.chat_join_request.from_user

    print(f"{user.username} joined")

    await context.bot.approve_chat_join_request(
        chat_id=CHANNEL_ID,
        user_id=user.id
    )

    await asyncio.sleep(60)

    await context.bot.ban_chat_member(
        chat_id=CHANNEL_ID,
        user_id=user.id
    )

    print(f"{user.username} removed")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(ChatJoinRequestHandler(joined))

print("Bot running...")
app.run_polling()
