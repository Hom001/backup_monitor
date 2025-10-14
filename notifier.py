import telebot
import os
from typing import List
from dotenv import load_dotenv


class TelegramNotifier:
    def __init__(self, header: str = f"{'*'*15} МОНИТОРИНГ БЭКАПОВ {'*'*15}"):
        load_dotenv()
        token = os.getenv("BOT_API_TOKEN")
        chat_id = os.getenv("MY_CHAT_ID")

        if not token or not chat_id:
            raise ValueError("BOT_API_TOKEN и MY_CHAT_ID должны быть заданы в .env файле.")
        
        self.bot = telebot.TeleBot(token)
        self.chat_id: str = str(chat_id)
        self.header = header

    def send_message(self, messages: List[str]):
        # отправка заголовка
        self.bot.send_message(self.chat_id, self.header)

        for msg in messages:
            self.bot.send_message(self.chat_id, msg)