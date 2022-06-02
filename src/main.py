import logging
import logging.config
import os

import yaml
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler


def read_config():
    with open("config.yml") as f:
        return yaml.safe_load(f)


config = read_config()

logger = logging.getLogger(__name__)
logging.config.dictConfig(config["logging"])


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    logger.info(
        f"Start command from user {update.effective_user.username}({update.effective_user.id})"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="ЖАННА АРКАДЬЕВНА!"
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(config["tg_token"]).build()

    start_handler = CommandHandler("start", start)
    app.add_handler(start_handler)
    app.run_polling()
