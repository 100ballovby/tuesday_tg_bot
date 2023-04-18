import os
import telebot

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


if __name__ == '__main__':
    bot.polling()
