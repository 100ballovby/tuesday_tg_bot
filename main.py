import os
import telebot
import functions

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def hello_message(message):
    template = functions.make_template('templates/start.html')
    username = message.chat.username
    msg_text = template.render(name=username)
    bot.send_message(message.chat.id, text=msg_text, parse_mode='html')


if __name__ == '__main__':
    bot.polling()
