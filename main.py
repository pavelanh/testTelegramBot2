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
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message.text,
        temperature=0.5,
        max_tokens=4000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    print(response)
    bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])


bot.infinity_polling()
