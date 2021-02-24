import os
import vk_api as vk
import random
import logging
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from google.cloud import dialogflow
from tg_bot import TelegramLogsHandler
from telegram import Bot


logger = logging.getLogger('chatbots-logger')


def answer(event, vk_api):
    project_id = os.getenv("PROJECT_ID")
    session_id = os.getenv("SESSION_ID")
    text, response = detect_intent_texts(
        project_id, session_id, event.text, 'ru-RU')
    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    return response.query_result.fulfillment_text, response


def main():
    load_dotenv()
    tg_token = os.getenv("TG_BOT_TOKEN")
    tg_user_id = os.getenv("TG_USER_ID")
    tg_bot = Bot(tg_token)
    logger = logging.getLogger('chatbots-logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_user_id))

    vk_session = vk.VkApi(token=os.getenv("VK_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api)


if __name__ == '__main__':
    main()
