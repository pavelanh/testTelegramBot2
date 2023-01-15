import logging
import re
import time

import openai
import telebot
from jproperties import Properties

import logger


def _get_property(prop):
    configs = Properties()
    with open('app-config.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get(prop).data


bot = telebot.TeleBot(_get_property('BOT_TOKEN'))
openai.api_key = _get_property('OPENAI_API_KEY')

OPT_MENU = {'Option 1', 'Option 2', 'Option 3'}


def run_telegram_bot():
    @bot.message_handler(func=lambda msg: True)
    def handle_message(message):
        text_from_request: str = message.text
        logging.info(f'You: {text_from_request}')
        if '/menu' == text_from_request:
            markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
            item_btn1 = telebot.types.KeyboardButton('Option 1')
            item_btn2 = telebot.types.KeyboardButton('Option 2')
            item_btn3 = telebot.types.KeyboardButton('Option 3')
            markup.add(item_btn1, item_btn2, item_btn3)

            bot.send_message(chat_id=message.chat.id, text="Choose one option:", reply_markup=markup)
        else:
            if text_from_request not in OPT_MENU:
                try:
                    response = create_bot_response(text_from_request)
                    send_message_to_chat_and_log(message, response)
                except openai.error.RateLimitError as err:
                    logging.error(f'Error: {err.user_message}')
                    bot.send_message(chat_id=message.from_user.id, text="I'm a little tired, give me a few seconds..")
                except Exception as exc:
                    logging.error(f'Error: \n{exc.__cause__}')
                    bot.send_message(chat_id=message.from_user.id, text="Give me 5 seconds to recover. Zzz..")
                    time.sleep(5)
                finally:
                    print('--------------------------')
            else:
                # Process the selected option
                bot.reply_to(message, 'You chose ' + message.text)

    def create_bot_response(text_from_request):
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=text_from_request,
            temperature=0.5,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        return response

    def send_message_to_chat_and_log(message, response):
        text_from_bot_response = response['choices'][0]['text']
        bot_response_to_print = re.sub('\n+', ' ', text_from_bot_response)
        logging.info(f'Bot:{bot_response_to_print}')
        bot.send_message(chat_id=message.from_user.id, text=text_from_bot_response)

    bot.polling()


if __name__ == '__main__':
    logger.setup_logging()
    run_telegram_bot()
