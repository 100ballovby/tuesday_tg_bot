import os
import telebot
import functions

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def hello_message(message):
    template = functions.make_template('templates/start.html')
    username = message.chat.username
    msg_text = template.render(name=username)
    pin = bot.send_message(message.chat.id, text=msg_text, parse_mode='html')  # сохраняем сообщение в переменной
    bot.pin_chat_message(message.chat.id, message_id=pin.id)  # закрепляем в чате сообщение бота


@bot.message_handler(commands=['help'])
def help_message(message):
    template = functions.make_template('templates/help.html')
    msg_text = template.render()
    bot.send_message(message.chat.id, text=msg_text, parse_mode='html')


@bot.message_handler(commands=['dog'])
def send_dog(message):
    img = functions.send_image()
    bot.send_photo(message.chat.id, photo=img)


@bot.message_handler(commands=['meme'])
def send_meme(message):
    img = functions.send_meme()
    bot.send_photo(message.chat.id, photo=img)


if __name__ == '__main__':
    bot.polling()
