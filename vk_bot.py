import os
import vk_api as vk
import random
import logging
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from logs_handler import TelegramLogsHandler
from telegram import Bot
from detect_intent import detect_intent_texts


logger = logging.getLogger('chatbots-logger')


def answer(event, vk_api):
    project_id = os.getenv("PROJECT_ID")
    session_id = os.getenv("SESSION_ID")
    intent = detect_intent_texts(
        project_id, session_id, event.text, 'ru-RU')
    if not intent.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=intent.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


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
