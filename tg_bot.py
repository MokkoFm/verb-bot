import os
import logging
from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
from logs_handler import TelegramLogsHandler


logger = logging.getLogger('chatbots-logger')


def start(bot, update):
    update.message.reply_text('Hi! Chatbot is activated!')


def answer(bot, update):
    project_id = os.getenv("PROJECT_ID")
    session_id = os.getenv("SESSION_ID")
    text = detect_intent_texts(project_id, session_id, update.message.text, 'ru-RU')
    bot.send_message(chat_id=update.message.chat_id, text=text)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)

    return response.query_result.fulfillment_text


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
