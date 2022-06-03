import logging
import logging.config

import yaml
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

products = []
PRODUCTS = range(1)


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


async def insert_product_start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Введите продукты"
    )
    return PRODUCTS


async def insert_product(update: Update, context: CallbackContext.DEFAULT_TYPE):
    msg = update.message.text
    reply = "Продукты успешно добавлены!"

    logger.info("Insert product command")
    logger.info(f"Input: {msg}")
    try:
        for msg in msg.split("\n"):
            product = msg.split()[0]
            expiration_date = msg.split()[1]
            products.append(tuple((product, expiration_date)))
    except IndexError:
        reply = "Ошибка! Формат ввода данных: <продукт> <дата окончания срока годности>"
        logger.error("Incorrect number of arguments in insert command")

    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

    return ConversationHandler.END


async def select_product(update: Update, context: CallbackContext.DEFAULT_TYPE):
    logger.info("Select product command")

    if products:
        products_msg = f"Продукты({len(products)}): \n" + "\n".join(
            f"{p[0]} {p[1]}" for p in products
        )
    else:
        products_msg = "<Пусто>"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=products_msg)


async def cancel_product(update: Update, context: CallbackContext.DEFAULT_TYPE):
    logger.info("Cancel the process of adding products")

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Отмена добавления продуктов"
    )

    return ConversationHandler.END


if __name__ == "__main__":
    app = ApplicationBuilder().token(config["tg_token"]).build()

    start_handler = CommandHandler("start", start)
    select_handler = CommandHandler("select", select_product)

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("insert", insert_product_start)],
        states={
            PRODUCTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, insert_product)],
        },
        fallbacks=[CommandHandler("cancel", cancel_product)],
    )

    app.add_handler(start_handler)
    app.add_handler(select_handler)
    app.add_handler(conversation_handler)

    app.run_polling()
