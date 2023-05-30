import os
import telebot
import functions
import csv

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


@bot.message_handler(commands=['weather'])
def show_buttons(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = telebot.types.KeyboardButton('Поделиться локацией', request_location=True)
    markup.add(btn)
    bot.send_message(message.chat.id, 'Поделись со мной своей локацией, пожалуйста.', reply_markup=markup)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    if message.location is not None:
        bot.send_message(message.chat.id, message.chat.id)
        weather = functions.get_weather(message.location.latitude, message.location.longitude)
        bot.send_message(message.chat.id, text=weather, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['register'])
def get_contacts(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = telebot.types.KeyboardButton('Отправить контакты', request_contact=True)
    markup.add(btn)
    bot.send_message(message.chat.id, 'Поделись со мной своими контактами',
                     reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def send_contact(message):
    if message.contact is not None:
        with open('contacts.csv', 'a') as file:
            writer = csv.writer(file)
            user = message.contact
            writer.writerow([user.first_name + ' ' + user.last_name,
                             user.phone_number, user.user_id])
        bot.send_message(message.chat.id, 'Спасибо!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['horo'])
def ask_zodiac(message):
    signs = ['Aries ♈️', 'Taurus ♉️', 'Gemini ♊️', 'Cancer ♋️',
             'Leo ♌️', 'Virgo ♍️', 'Libra ♎️', 'Scorpio ♏️',
             'Sagittarius ♐️', 'Capricorn ♑️', 'Aquarius ♒️', 'Pisce ♓️']
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    buttons = [telebot.types.KeyboardButton(sign) for sign in signs]

    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Выбери свой знак зодиака: ', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_horo(message):
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer',
             'Leo', 'Virgo', 'Libra', 'Scorpio',
             'Sagittarius', 'Capricorn', 'Aquarius', 'Pisce']
    if message.text[:-3] in signs:
        zodiac_sign = message.text[:-3]
        res = functions.get_horo(zodiac_sign.lower())
        bot.send_message(message.chat.id, text=res)



if __name__ == '__main__':
    bot.polling()
