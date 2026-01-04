import logging
import os
import requests

from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()

TOKEN = os.getenv('TOKEN_YESNO')
bot = TeleBot(token=TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s - %(name)s',
    level=logging.INFO,
    filename='yesnobot.log'
)

URL = 'https://yesno.wtf/api'


def get_new_answer(URL):
    try:
        response = requests.get(URL).json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
    answer = list()
    text_answer = response.get('answer')
    if text_answer == 'yes':
        answer.append('Да.')
    elif text_answer == 'no':
        answer.append('Нет.')
    else:
        answer.append(r'Может быть. \_(0_0)_/')
    image_answer = response.get('image')
    answer.append(image_answer)
    return answer


@bot.message_handler(func=lambda message: message.text == 'Случайный ответ')
def random_answer_from_button(message):
    chat = message.chat
    answer = get_new_answer(URL)

    bot.send_message(chat_id=chat.id, text=answer[0])
    bot.send_animation(chat_id=chat.id, animation=answer[1])


@bot.message_handler(func=lambda message: message.text == 'Да ✅')
def yes_answer_from_button(message):
    chat = message.chat

    force_url = URL + '?force=yes'
    answer = get_new_answer(force_url)

    bot.send_message(chat_id=chat.id, text=answer[0])
    bot.send_animation(chat_id=chat.id, animation=answer[1])


@bot.message_handler(func=lambda message: message.text == 'Нет ❌')
def no_answer_from_button(message):
    chat = message.chat
    answer = get_new_answer(URL)

    force_url = URL + '?force=no'
    answer = get_new_answer(force_url)

    bot.send_message(chat_id=chat.id, text=answer[0])
    bot.send_animation(chat_id=chat.id, animation=answer[1])


@bot.message_handler(func=lambda message: message.text == 'Может быть 😏')
def maybe_answer_from_button(message):
    chat = message.chat
    answer = get_new_answer(URL)

    force_url = URL + '?force=maybe'
    answer = get_new_answer(force_url)

    bot.send_message(chat_id=chat.id, text=answer[0])
    bot.send_animation(chat_id=chat.id, animation=answer[1])


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_randomanswer = types.KeyboardButton('Случайный ответ')
    button_yesanswer = types.KeyboardButton('Да ✅')
    button_noanswer = types.KeyboardButton('Нет ❌')
    button_maybeanswer = types.KeyboardButton('Может быть 😏')
    keyboard.add(button_randomanswer, row_width=1)
    keyboard.add(
        button_yesanswer,
        button_noanswer,
        button_maybeanswer,
        row_width=3
    )

    bot.send_message(
        chat_id=chat.id,
        text='Мысленно задай вопрос и получи ответ.',
        reply_markup=keyboard,
    )


def main():
    bot.polling()


if __name__ == '__main__':
    main()
