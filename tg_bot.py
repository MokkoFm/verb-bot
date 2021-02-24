import os
import logging
from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot


logger = logging.getLogger('chatbots-logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(bot, update):
    """Send a message when the command /start is issued."""
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
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    tg_token = os.getenv("TG_BOT_TOKEN")
    tg_user_id = os.getenv("TG_USER_ID")
    tg_bot = Bot(tg_token)
    logger = logging.getLogger('chatbots-logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_user_id))
    updater = Updater(tg_token)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, answer))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
