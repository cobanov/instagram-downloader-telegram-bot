import logging
import re
from telegram import Update
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from instagram_helpers import download_and_send_instagram_post
from dotenv import load_dotenv
import os

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)

load_dotenv()
TOKEN = my_id = os.getenv("TOKEN")
logging.warning(f"Telegram version: {telegram.__version__}")


async def start(update: Update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def download_instagram(update: Update, context):
    message = update.message.text
    if re.match(r"(https?://)?(www\.)?instagram\.com/(p|reel)/.+", message):
        await download_and_send_instagram_post(message, update, context)
    else:
        await update.message.reply_text("Please send a valid Instagram post URL.")


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download_instagram)
    )

    application.run_polling()


if __name__ == "__main__":
    main()
