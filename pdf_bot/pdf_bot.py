from pdf_editor import *
from bs4 import BeautifulSoup
from datetime import datetime
import telebot
import sqlite3
from os import remove, mkdir, path, listdir, removedirs
from secrets import choice, token_hex

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


TOKEN = "1654109240:AAHNYRyKZJTJjpikeBCng40XTm9t8oVtTmw"
bot = telebot.TeleBot(TOKEN)



@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(callback_query_id=call.id, text='Answer accepted!')

    print(call.data)
    if call.data == "True":
        bot.send_message(call.message.chat.id, "type the filename below")
        bot.edit_message_reply_markup(chat_id, call.message.message_id)
    else:
        try:
            filename = str(chat_id) + '.pdf'
            bot.send_message(chat_id, 'processing...')
            files = listdir(str(chat_id))
            data = list()
            for i in files:
                if '.jpg' not in i: 
                    data.append(i)
            
            pdfs_merger(data, filename, str(chat_id))
            bot.send_document(chat_id, open(filename, 'rb'))
            for i in files:
                remove(f'{str(chat_id)}\\{i}')
            try:
                remove(str(chat_id) + '\\' + str(chat_id) + '.pdf')
            except:
                pass
            removedirs(str(chat_id))
        except FileNotFoundError:
            bot.reply_to(call.message, 'send photos first!')


@bot.message_handler(commands=['pdf'])
@bot.message_handler(regexp='^/pdf')
def pdf_converter(message):
    # if message.chat.type == 'private': 
        print(message.text)
        chat_id = message.chat.id

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Yes', callback_data="True"))
        markup.add(telebot.types.InlineKeyboardButton(text='No', callback_data="False"))
        mes = bot.send_message(message.chat.id, text="Do You Want To Set A Filename?", reply_markup=markup)
        bot.register_next_step_handler(mes, mero)


@bot.message_handler(content_types=['photo'])
def img_handler(message):
    # if message.chat.type == 'private': 
        chat_id = message.chat.id
        try:
            mkdir(str(chat_id))
        except FileExistsError:
            pass
    
        n = token_hex(14)

        obj = download_photo(TOKEN, message.photo, str(chat_id), f'image{n}.jpg', chat_id)
        image_data = message.photo[obj.get_best_rez()[-1]]
        img_name = obj.main()

        img2pdf_conv(img_name, img_name[: img_name.index('.')] + '.pdf', {'height':image_data.height, 'width':image_data.width}).main()
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.InlineKeyboardButton('/pdf'))
        d = bot.send_message(message.chat.id, 'Press the button on the keyboard or send another photo:', reply_markup=keyboard, timeout=0.7)

        bot.register_next_step_handler(d, leor, d)


def mero(message):
    chat_id = message.chat.id
    text = message.text
    if '.pdf' in text:
        filename = f'{str(chat_id)}\\{text}'
    else:
        filename = f'{str(chat_id)}\\{text}.pdf'
        
    bot.send_message(chat_id, 'processing...')
    files = listdir(str(chat_id))
    data = list()
    for i in files:
        if '.jpg' not in i:
            data.append(i)
    
    pdfs_merger(data, filename, str(message.chat.id))
    bot.send_document(chat_id, open(filename, 'rb'))
    for i in files:
        remove(f'{str(chat_id)}\\{i}')
    try:
        remove(filename)
    except:
        pass
    removedirs(str(chat_id))


def leor(message, d):
    if message.content_type != 'text':
        bot.delete_message(message.chat.id, d.message_id)
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.InlineKeyboardButton('ready2convert', callback_data='/pdf'))
        d = bot.send_message(message.chat.id, 'Press the button on the keyboard or send another photo:', reply_markup=keyboard)
