import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
from logs_handler import TelegramLogsHandler
from detect_intent import detect_intent_texts


logger = logging.getLogger('chatbots-logger')


def start(bot, update):
    update.message.reply_text('Hi! Chatbot is activated!')


def answer(bot, update):
    project_id = os.getenv("PROJECT_ID")
    session_id = f'tg-{update.message.chat_id}'
    intent = detect_intent_texts(
        project_id, session_id, update.message.text, 'ru-RU')
    bot.send_message(
        chat_id=update.message.chat_id, text=intent.fulfillment_text)


def main():
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    tg_user_id = os.getenv("TG_USER_ID")
    tg_bot = Bot(tg_token)
    logger = logging.getLogger('chatbots-logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_user_id))
    updater = Updater(tg_token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
