from django.core.management.base import BaseCommand
from django.conf import settings
from config.settings import BOT_TOKEN

from telebot import TeleBot, types

# Объявление переменной бота
bot = TeleBot(BOT_TOKEN, threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Just a command for launching a Telegram bot.'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.infinity_polling(skip_pending=True)  # Бесконечный цикл бота


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
    'text', 'location', 'contact', 'sticker'])
def start_message(message):
    chat_id = message.chat.id
    message_id = message.id
    text = f"Поместите следующий код в поле «Код публикации» при создании публикации.\n```{chat_id},{message_id}```"
    bot.send_message(chat_id=message.chat.id, text=text, reply_to_message_id=message_id, parse_mode="Markdown")
