import telebot
from typing import List

from core.settings import settings


class TelegramNotifier:
    def __init__(self, header: str = f"{'*'*15} МОНИТОРИНГ БЭКАПОВ {'*'*15}"):
        token = settings.BOT_API_TOKEN
        chat_id = settings.MY_CHAT_ID

        if not token or not chat_id:
            raise ValueError("BOT_API_TOKEN и MY_CHAT_ID должны быть заданы в .env файле.")
        
        self.bot = telebot.TeleBot(token)
        self.chat_id: str = str(chat_id)
        self.header = header

    def send_messages(self, messages: List[str]):
        # отправка заголовка
        self.bot.send_message(self.chat_id, self.header)

        for msg in messages:
            self.bot.send_message(self.chat_id, msg)