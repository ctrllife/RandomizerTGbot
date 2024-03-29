import telebot
import config
from words import words
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)



@bot.message_handler(commands=['start'])
def welcome(message):
    sticker_welcome = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker_welcome)

    # клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('🎲 Рандомное число')
    item_2 = types.KeyboardButton('💬 Рандомные фразы')

    markup.add(item_1, item_2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, <b>{0.first_name}</b>!\nЯ - Telegram бот <b>{1.first_name}</b>, который умеет:\n • Выдавать рандомное число просто, а также из определённого промежутка;\n • Выводить любую фразу или цитату известных людей;\nПогнали!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item_1 = types.InlineKeyboardButton('Без ограничений', callback_data='none_stop')
            item_2 = types.InlineKeyboardButton('С границами рандома 🎲', callback_data='stop')

            markup.add(item_1, item_2)

            bot.send_message(message.chat.id, f'Выберите вариант ограничения рандомайзера:', reply_markup=markup)
        elif message.text == '💬 Рандомные фразы':
            #bot.send_message(message.chat.id, 'Извините, пока что функция недоступна 😭')
            markup = types.InlineKeyboardMarkup(row_width=2)
            item_1 = types.InlineKeyboardButton('Эйнштейн', callback_data='einshtein')
            item_2 = types.InlineKeyboardButton('Суворов', callback_data='suvorov')
            item_3 = types.InlineKeyboardButton('Любой', callback_data='luboy')
            item_4 = types.InlineKeyboardButton('Линкольн', callback_data='lincoln')
            item_5 = types.InlineKeyboardButton('Шекспир', callback_data='shekspir')
            item_6 = types.InlineKeyboardButton('Экзюпери', callback_data='ekzuperi')

            markup.add(item_1, item_2, item_4, item_5, item_6, item_3)
            bot.send_message(message.chat.id, f'Выберите чью фразу вы хотите увидеть: ', reply_markup=markup)
        elif message.text.isdigit():
            bot.send_message(message.chat.id, f'Ваше рандомное число - {str(random.randint(1, int(message.text)))}')
        else:
            bot.send_message(message.chat.id, f'Я не знаю такой функции 😭')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'none_stop':
                bot.send_message(call.message.chat.id, f'Ваше рандомное число - {str(random.randint(1, 10000))}')
            if call.data == 'stop':
                bot.send_message(call.message.chat.id,
                                 f'Введите границу диапазона сообщением в виде: \n25\n<b>Учтите, что начальная граница уже выставлена по умолчанию(1)</b>',
                                 parse_mode='html')
            if call.data == 'einshtein':
                otvet = words['Эйнштейн']
                bot.send_message(call.message.chat.id, f'А. Эйнштейн говорил: "{random.choice(otvet)}"')
            if call.data == 'suvorov':
                otvet = words['Суворов']
                bot.send_message(call.message.chat.id, f'А. В. Суворов говорил: "{random.choice(otvet)}"')
            if call.data == 'lincoln':
                otvet = words['Линкольн']
                bot.send_message(call.message.chat.id, f'А. Линкольн говорил: "{random.choice(otvet)}"')
            if call.data == 'shekspir':
                otvet = words['Шекспир']
                bot.send_message(call.message.chat.id, f'В. Шекспир говорил: "{random.choice(otvet)}"')
            if call.data == 'ekzuperi':
                otvet = words['Экзюпери']
                bot.send_message(call.message.chat.id, f'Антуан де Сент-Экзюпери говорил: "{random.choice(otvet)}"')
            if call.data == 'luboy':
                key = random.choice(list(words.keys()))
                otvet = words[key]
                bot.send_message(call.message.chat.id, f'{key} говорил: "{random.choice(otvet)}"')

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
