import re
import time

import openai
import telebot
from jproperties import Properties


def __get_property(prop):
    configs = Properties()
    with open('app-config.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get(prop).data


bot = telebot.TeleBot(__get_property('BOT_TOKEN'))
openai.api_key = __get_property('OPENAI_API_KEY')


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    text_from_request = message.text
    try:
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=text_from_request,
            temperature=0.5,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        print(f'You: {text_from_request}')
        text_from_bot_response = response['choices'][0]['text']
        bot_response_to_print = re.sub('\n+', ' ', text_from_bot_response)
        print(f"Bot:{bot_response_to_print}")
        bot.send_message(chat_id=message.from_user.id, text=text_from_bot_response)
    except openai.error.RateLimitError as err:
        print(f'Error: {err.user_message}')
        bot.send_message(chat_id=message.from_user.id, text="I'm a little tired, give me a few seconds..")
    except Exception as exc:
        print(f'Error: \n{exc.__cause__}')
        bot.send_message(chat_id=message.from_user.id, text="Give me 5 seconds to recover. Zzz..")
        time.sleep(5)
    finally:
        print('--------------------------')


bot.polling()
