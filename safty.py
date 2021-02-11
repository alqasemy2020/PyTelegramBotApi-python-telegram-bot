from bs4 import BeautifulSoup
from datetime import datetime 
from telegram import Update
from threading import Thread
from requests import get, post
import telebot
import sqlite3
import re
import sys
import telegram
from pytz import timezone

TOKEN = '1678451741:AAERn9MzVZT7YM5Zfl_o3coJVwFXEYYgsjM'
bot = telebot.TeleBot(TOKEN)
sudo = 1402010763
dev = [942683545,1207564961,1405097902]
###########################private###########################
def ex_id(id):
    result = False
    filerdr = open("users.txt","r")
    for line in filerdr:
        if line.strip()==id:
            result = True
    filerdr.close()
    return result

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try :
        keyboard = [
                    [
                        InlineKeyboardButton("المطور", "https://t.me/yloxr" , callback_data="main_dev")
                    ]
                ]

        reply_wel = telebot.types.InlineKeyboardMarkup(keyboard)

        

        if message.chat.type == 'private':
            id_num = message.from_user.id
            cunt = open("users.txt","a")
            if (not ex_id(str(id_num))):
                cunt.write("{}\n".format(id_num))
                cunt.close()
                bot.send_message(message.chat.id,welcome,reply_markup=reply_wel)
                


            else : 
                bot.send_message(message.chat.id ,"أهلا بك مجددا🤍")
                bot.send_message(message.chat.id,welcome,reply_markup=reply_wel)
    except : bot.reply_to(message,"• عذرا لقد حصل خطأ\n• يرجى التواصل مع االمطور لحل المشكلة\n • المطور ===> @yloxr")

@bot.message_handler(commands=['users'])
def detusrs(message):
    try :
        if message.chat.type == 'private':
            filerdr = open("users.txt","r")
            us = len(filerdr.readlines())
            bot.reply_to(message,"*users :* {}".format(us),parse_mode="markdown")
        else : pass
    except : bot.reply_to(message,"• عذرا لقد حصل خطأ\n• يرجى التواصل مع االمطور لحل المشكلة\n • المطور ===> @yloxr")

@bot.message_handler(commands=["features"])
def features(message):
    try :
        bot.reply_to(message,features)
    except : bot.reply_to(message,"• عذرا لقد حصل خطأ\n• يرجى التواصل مع االمطور لحل المشكلة\n • المطور ===> @yloxr")
    
###########################private###########################

def time_json():
    content = get('https://hijri-calendar.com/').content.decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    date_hijri = soup.find(class_='today').find(class_='hijri').text
    today_ar = soup.find(class_='today').find(class_='meladi').text
    date_meladi = soup.find(class_='today').find_all(class_='meladi')[-1].text
    today_en = datetime.now(timezone('Asia/Riyadh')).strftime('%a')
    return {'date_hijri':date_hijri, 'date_meladi':date_meladi, 'today_ar':today_ar, 'today_en': today_en}


def chk_rank(cht_id, id_num):
    conn = sqlite3.connect(f'{cht_id}.db')
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS ranks (
        id_num intger ,
        rank text)""")
    c.execute(""" CREATE TABLE IF NOT EXISTS settings (
        setting text ,
        status text)""")
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    if id_num == sudo :
        rank = "main_dev"
        rank_txt = "المطور الأساسي 👨‍✈️🧳"
    elif id_num in dev :
        rank = "dev"
        rank_txt = "مطور 🧑‍💻"
    elif (id_num,"main_creator") in pranks :
        rank = "main_creator"
        rank_txt = "الملك 👑"
    elif (id_num,"creator") in pranks :
        rank = "creator"
        rank_txt = "نائب الملك 🧑🏼‍💼"
    elif (id_num,"boss") in pranks :
        rank = "boss"
        rank_txt = "أمير 💍"
    elif (id_num,"admin") in pranks :
        rank = "admin"
        rank_txt = "نائب الأمير 🧑🏼‍💼"
    elif (id_num,"special") in pranks :
        rank = "special"
        rank_txt = "مميز 🤩"
    else : 
        rank = "member" 
        rank_txt = "عضو 🙇‍♂️"
    conn.commit()
    conn.close()
    return [rank, rank_txt]


@bot.message_handler(regexp="^فتح")
def open(message):
        text = message.text
        msg_id = message.id
        id_num = message.from_user.id
        cht_id = message.chat.id
        rank = chk_rank(cht_id,id_num)[0]
        rank_txt = chk_rank(cht_id, id_num)[1]

        if text == "فتح الدردشه" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("chat","locked") not in pranks and ("chat","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('chat','opened')")
                    bot.reply_to(message,"تم فتح الدردشة 🔓🖋")
                else : 
                    c.execute("UPDATE settings SET status = 'opened' WHERE setting = 'chat'")
                    bot.reply_to(message,"تم فتح الدردشة 🔓🖋")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "فتح الملصقات" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("stickers","locked") not in pranks and ("stickers","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('stickers','opened')")
                    bot.reply_to(message,"تم قفل الملصقات 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'opened' WHERE setting = 'stickers'")
                    bot.reply_to(message,"تم قفل الملصقات 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "فتح المتحركه" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("gif","locked") not in pranks and ("gif","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('gif','opened')")
                    bot.reply_to(message,"تم قفل المتحركة 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'opened' WHERE setting = 'gif'")
                    bot.reply_to(message,"تم قفل المتحركة 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "فتح الصور" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("photos","locked") not in pranks and ("photos","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('photos','opened')")
                    bot.reply_to(message,"تم قفل المتحركة 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'opened' WHERE setting = 'photos'")
                    bot.reply_to(message,"تم قفل المتحركة 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "فتح الفيديو" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("videos","locked") not in pranks and ("videos","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('videos','opened')")
                    bot.reply_to(message,"تم قفل الفيديو 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'opened' WHERE setting = 'videos'")
                    bot.reply_to(message,"تم قفل الفيديو 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "فتح الجهات" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("contacts","locked") not in pranks and ("contacts","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('contacts','opened')")
                    bot.reply_to(message,"تم قفل الجهات 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'opened' WHERE setting = 'contacts'")
                    bot.reply_to(message,"تم قفل الجهات 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "فتح الموقع" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("locations","locked") not in pranks and ("locations","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('locations','opened')")
                    bot.reply_to(message,"تم قفل الموقع 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'opened' WHERE setting = 'locations'")
                    bot.reply_to(message,"تم قفل الموقع 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "فتح الملفات" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("documents","locked") not in pranks and ("documents","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('documents','opened')")
                    bot.reply_to(message,"تم قفل الملفات 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'opened' WHERE setting = 'documents'")
                    bot.reply_to(message,"تم قفل الملفات 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "فتح الالعاب" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("games","locked") not in pranks and ("games","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('games','opened')")
                    bot.reply_to(message,"تم قفل الالعاب 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'opened' WHERE setting = 'games'")
                    bot.reply_to(message,"تم قفل الالعاب 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")


@bot.message_handler(regexp="^قفل")
def open(message):
        text = message.text
        msg_id = message.id
        id_num = message.from_user.id
        cht_id = message.chat.id
        rank = chk_rank(cht_id, id_num)[0]
        rank_txt = chk_rank(cht_id,id_num)[1]
        if text == "قفل الدردشه" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("chat","locked") not in pranks and ("chat","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('chat','locked')")
                    bot.reply_to(message,"تم قفل الدردشة 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'locked' WHERE setting = 'chat'")
                    bot.reply_to(message,"تم قفل الدردشة 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "قفل الملصقات" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("stickers","locked") not in pranks and ("stickers","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('stickers','locked')")
                    bot.reply_to(message,"تم قفل الملصقات 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'locked' WHERE setting = 'stickers'")
                    bot.reply_to(message,"تم قفل الملصقات 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "قفل المتحركه" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("gif","locked") not in pranks and ("gif","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('gif','locked')")
                    bot.reply_to(message,"تم قفل المتحركة 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'locked' WHERE setting = 'gif'")
                    bot.reply_to(message,"تم قفل المتحركة 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "قفل الصور" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("photos","locked") not in pranks and ("photos","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('photos','locked')")
                    bot.reply_to(message,"تم قفل الصور 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'locked' WHERE setting = 'photos'")
                    bot.reply_to(message,"تم قفل الصور 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "قفل الفيديو" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("videos","locked") not in pranks and ("videos","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('videos','locked')")
                    bot.reply_to(message,"تم قفل الفيديو 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'locked' WHERE setting = 'videos'")
                    bot.reply_to(message,"تم قفل الفيديو 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "قفل الجهات" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("contacts","locked") not in pranks and ("contacts","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('contacts','locked')")
                    bot.reply_to(message,"تم قفل الجهات 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'locked' WHERE setting = 'contacts'")
                    bot.reply_to(message,"تم قفل الجهات 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "قفل الموقع" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("locations","locked") not in pranks and ("locations","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('locations','locked')")
                    bot.reply_to(message,"تم قفل الفيديو 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'locked' WHERE setting = 'locations'")
                    bot.reply_to(message,"تم قفل الفيديو 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "قفل الملفات" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("documents","locked") not in pranks and ("documents","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('documents','locked')")
                    bot.reply_to(message,"تم قفل الملفات 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'locked' WHERE setting = 'documents'")
                    bot.reply_to(message,"تم قفل الملفات 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")
        elif text == "قفل الالعاب" :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                conn = sqlite3.connect(f'{cht_id}.db')
                c = conn.cursor()
                c.execute("SELECT * FROM settings")
                pranks = c.fetchall()
                if ("games","locked") not in pranks and ("games","opened") not in pranks :
                    c.execute("INSERT INTO settings VALUES ('games','locked')")
                    bot.reply_to(message,"تم قفل الفيديو 🔏")
                else : 
                    c.execute("UPDATE settings SET status = 'locked' WHERE setting = 'games'")
                    bot.reply_to(message,"تم قفل الفيديو 🔏")
                conn.commit()
                conn.close()
            else : bot.reply_to(message,"sorry but you don't have permission 😊")


@bot.message_handler(regexp="^رفع")
def rnkup(message):
    text = message.text
    msg_id = message.id
    id_num = message.from_user.id
    cht_id = message.chat.id
    rank = chk_rank(cht_id, id_num)[0]
    rank_txt = chk_rank(cht_id,id_num)[1]
    if text == "رفع مطور":
        if rank == "main_dev":
            bot.reply_to(message,"You should add the developer manually🛠")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
    elif text == "رفع ملك" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")    
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" :
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"main_creator") in pranks :
                    bot.reply_to(message,"هو بالفعل ملك 👑")
                else:
                    c.execute(f"INSERT INTO ranks VALUES ({int(nw_rank)},'main_creator')")
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتمت ترقيته ليصبح الملك 👑\nبواسطة | {rank_txt}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()
    elif text == "رفع نائب ملك" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks:
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"creator") in pranks :
                    bot.reply_to(message,"هو بالفعل نائب ملك😊")
                else:
                    c.execute(f"INSERT INTO ranks VALUES ({int(nw_rank)},'creator')")
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتمت ترقيته ليصبح نائباََ للملك 🧑🏼‍💼\nبواسطة| {rank_txt}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()
    elif text == "رفع امير" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks:
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"boss") in pranks :
                    bot.reply_to(message,"هو بالفعل أمير😊")
                else:
                    c.execute(f"INSERT INTO ranks VALUES ({int(nw_rank)},'boss')")
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتمت ترقيته ليصبح أميراً 💍\nبواسطة| {rank_txt}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()
    elif text == "رفع نائب امير" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks:
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"admin") in pranks :
                    bot.reply_to(message,"هو بالفعل نائب أمير😊")
                else:
                    c.execute(f"INSERT INTO ranks VALUES ({int(nw_rank)},'admin')")
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتمت ترقيته ليصبح نائباً للأمير 🧑🏼‍💼\nبواسطة| {rank_txt}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()
    elif text == "رفع مميز" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"special") in pranks :
                    bot.reply_to(message,"هو بالفعل مميز😊")
                else:
                    c.execute(f"INSERT INTO ranks VALUES ({int(nw_rank)},'special')")
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتمت ترقيته ليصبح عضواً مميزا 🤩\nبواسطة| {rank_txt}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()


@bot.message_handler(regexp="^تنزيل")
def rnkdwn(message):
    text = message.text
    msg_id = message.id
    id_num = message.from_user.id
    cht_id = message.chat.id
    rank = chk_rank(cht_id, id_num)[0]
    rank_txt = chk_rank(cht_id,id_num)[1]
    if text == "تنزيل مطور" :
        if rank == "main_dev":
            bot.reply_to(message,"You should add the developer manually🛠")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
    elif text == "تنزيل ملك" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" :
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"main_creator") not in pranks :
                    bot.reply_to(message,"انه بالفعل ليس ملك 👑")
                else :
                    delete_user('ranks', nw_rank, 'main_creator')
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتمت تنحيته من رتبة الملك👑\nبواسطة| {rank_txt}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()
    elif text == "تنزيل نائب ملك" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks:
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"creator") not in pranks :
                    bot.reply_to(message,"انه بالفعل ليس نائب ملك 🧑🏼‍💼")
                else :
                    delete_user('ranks', nw_rank, 'creator')
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتمت تنحيته من رتبة نائب الملك 🧑🏼‍💼\nبواسطة| {rank_txt}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()
    elif text == "تنزيل امير" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks:
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"boss") not in pranks :
                    bot.reply_to(message,"انه بالفعل ليس امير 💍")
                else :
                    delete_user('ranks', nw_rank, 'boss')
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتمت تنحيته من رتبة الأمير 💍\nبواسطة| {rank_txt}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()
    elif text == "تنزيل نائب امير" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks:
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"admin") not in pranks :
                    bot.reply_to(message,"انه بالفعل ليس نائب امير 🧑🏼‍💼")
                else :
                    delete_user('ranks', nw_rank, 'admin')
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتمت تنحيته من رتبة نائب الأمير 🧑🏼‍💼\nبواسطة| {rank_txt}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()
    elif text == "تنزيل مميز" :
        conn = sqlite3.connect(f'{cht_id}.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ranks")
        pranks = c.fetchall()
        if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
            if message.reply_to_message :
                nw_rank = message.reply_to_message.from_user.id
                if (nw_rank,"special") not in pranks :
                    bot.reply_to(message,"انه بالفعل ليس مميز 🧑‍⚖️")
                else :
                    delete_user('ranks', nw_rank, 'special')
                    bot.reply_to(message,f"تم تنزيله من رتبة المميز\nبواسطة | {rank_txt}")
            else: bot.send_message(message.chat.id,"who? 👀")
        else : bot.reply_to(message,"sorry but you don't have permission 😊")
        conn.commit()
        conn.close()

@bot.message_handler(regexp="^تقييد")
def restrict_1(message):
    text = message.text
    msg_id = message.id
    id_num = message.from_user.id
    cht_id = message.chat.id
    name = message.from_user.first_name
    rank = chk_rank(cht_id, id_num)[0]
    date_number = message.text.replace('تقييد', '').strip()
    print(date_number)
    if text == "تقييد":
        if message.reply_to_message :
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                id_num_2 = message.reply_to_message.from_user.id
                rank_2 = chk_rank(cht_id,id_num_2)[0]
                name_2 = message.reply_to_message.from_user.first_name
                if rank_2 == "main_dev" or rank_2 == "dev" or (id_num_2,"main_creator") in pranks or (id_num_2,"creator") in pranks or (id_num_2,"boss") in pranks or (id_num_2,"admin") in pranks:
                    bot.reply_to(message,"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nيمنع تقييد المشرفين 🔪🔪\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
                else : 
                    bot.restrict_chat_member(cht_id,id_num_2,None,False,False,None,False)
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتم   تقييد | {name_2}\nبواسطة     | {name}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.reply_to(message,"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nانت لا تمتلك الصلاحية للتقييد 🔪🔪\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")

    elif "دقيقة" in date_number:
        if message.reply_to_message :
            date = int(date.replace('دقيقة', '').strip())
            restrict_date = date*60
            time_restrict = message.date + restrict_date
            if rank == "main_dev" or rank == "dev" or (id_num,"main_creator") in pranks or (id_num,"creator") in pranks or (id_num,"boss") in pranks or (id_num,"admin") in pranks:
                id_num_2 = message.reply_to_message.from_user.id
                rank_2 = chk_rank(cht_id,id_num_2)[0]
                name_2 = message.reply_to_message.from_user.id
                if rank_2 == "main_dev" or rank_2 == "dev" or (id_num_2,"main_creator") in pranks or (id_num_2,"creator") in pranks or (id_num_2,"boss") in pranks or (id_num_2,"admin") in pranks:
                    bot.reply_to(message,"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nيمنع تقييد المشرفين 🔪🔪\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
                else : 
                    bot.restrict_chat_member(cht_id,id_num_2,time_restrict,False,False,None,False)
                    bot.reply_to(message,f"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nتم   تقييد | {name_2}\nبواسطة     | {name}\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")
            else: bot.reply_to(message,"ا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا\nانت لا تمتلك الصلاحية للتقييد 🔪🔪\nا♕♕♕♕♕♕♕♕♕♕♕♕♕♕ا")




@bot.message_handler(content_types=['sticker'])
def sticker_chk(message):
    id_num = message.from_user.id

    cht_id = message.chat.id
    msg_id = message.id
    conn = sqlite3.connect(f'{cht_id}.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    if id_num == sudo :
        rank = "main_dev"
        rank_txt = "المطور الأساسي 👨‍✈️🧳"
    elif id_num in dev :
        rank = "dev"
        rank_txt = "مطور 🧑‍💻"
    elif (id_num,"main_creator") in pranks :
        rank = "main_creator"
        rank_txt = "الملك 👑"
    elif (id_num,"creator") in pranks :
        rank = "creator"
        rank_txt = "نائب الملك 🧑🏼‍💼"
    elif (id_num,"boss") in pranks :
        rank = "boss"
        rank_txt = "أمير 💍"
    elif (id_num,"admin") in pranks :
        rank = "admin"
        rank_txt = "نائب الأمير 🧑🏼‍💼"
    elif (id_num,"special") in pranks :
        rank = "special"
        rank_txt = "مميز 🤩"
    else : 
        rank = "member" 
        rank_txt = "عضو 🙇‍♂️"
    c.execute("SELECT * FROM settings")
    pranks = c.fetchall()
    if rank == "member" :
        if ("stickers","locked") in pranks :
            bot.delete_message(cht_id,msg_id)
    conn.commit()
    conn.close()


@bot.message_handler(content_types=['photo'])
def sticker_chk(message):
    id_num = message.from_user.id
    cht_id = message.chat.id
    msg_id = message.id
    conn = sqlite3.connect(f'{cht_id}.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    if id_num == sudo :
        rank = "main_dev"
        rank_txt = "المطور الأساسي 👨‍✈️🧳"
    elif id_num in dev :
        rank = "dev"
        rank_txt = "مطور 🧑‍💻"
    elif (id_num,"main_creator") in pranks :
        rank = "main_creator"
        rank_txt = "الملك 👑"
    elif (id_num,"creator") in pranks :
        rank = "creator"
        rank_txt = "نائب الملك 🧑🏼‍💼"
    elif (id_num,"boss") in pranks :
        rank = "boss"
        rank_txt = "أمير 💍"
    elif (id_num,"admin") in pranks :
        rank = "admin"
        rank_txt = "نائب الأمير 🧑🏼‍💼"
    elif (id_num,"special") in pranks :
        rank = "special"
        rank_txt = "مميز 🤩"
    else : 
        rank = "member" 
        rank_txt = "عضو 🙇‍♂️"
    c.execute("SELECT * FROM settings")
    pranks = c.fetchall()
    if rank == "member" :
        if ("photos","locked") in pranks :
            bot.delete_message(cht_id,msg_id)
    conn.commit()
    conn.close()


@bot.message_handler(content_types=['video'])
def sticker_chk(message):
    id_num = message.from_user.id
    cht_id = message.chat.id
    msg_id = message.id
    conn = sqlite3.connect(f'{cht_id}.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    if id_num == sudo :
        rank = "main_dev"
        rank_txt = "المطور الأساسي 👨‍✈️🧳"
    elif id_num in dev :
        rank = "dev"
        rank_txt = "مطور 🧑‍💻"
    elif (id_num,"main_creator") in pranks :
        rank = "main_creator"
        rank_txt = "الملك 👑"
    elif (id_num,"creator") in pranks :
        rank = "creator"
        rank_txt = "نائب الملك 🧑🏼‍💼"
    elif (id_num,"boss") in pranks :
        rank = "boss"
        rank_txt = "أمير 💍"
    elif (id_num,"admin") in pranks :
        rank = "admin"
        rank_txt = "نائب الأمير 🧑🏼‍💼"
    elif (id_num,"special") in pranks :
        rank = "special"
        rank_txt = "مميز 🤩"
    else : 
        rank = "member" 
        rank_txt = "عضو 🙇‍♂️"
    c.execute("SELECT * FROM settings")
    pranks = c.fetchall()
    if rank == "member" :
        if ("videos","locked") in pranks :
            bot.delete_message(cht_id,msg_id)
    conn.commit()
    conn.close()


@bot.message_handler(content_types=['contact'])
def sticker_chk(message):
    id_num = message.from_user.id

    cht_id = message.chat.id
    msg_id = message.id
    conn = sqlite3.connect(f'{cht_id}.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    if id_num == sudo :
        rank = "main_dev"
        rank_txt = "المطور الأساسي 👨‍✈️🧳"
    elif id_num in dev :
        rank = "dev"
        rank_txt = "مطور 🧑‍💻"
    elif (id_num,"main_creator") in pranks :
        rank = "main_creator"
        rank_txt = "الملك 👑"
    elif (id_num,"creator") in pranks :
        rank = "creator"
        rank_txt = "نائب الملك 🧑🏼‍💼"
    elif (id_num,"boss") in pranks :
        rank = "boss"
        rank_txt = "أمير 💍"
    elif (id_num,"admin") in pranks :
        rank = "admin"
        rank_txt = "نائب الأمير 🧑🏼‍💼"
    elif (id_num,"special") in pranks :
        rank = "special"
        rank_txt = "مميز 🤩"
    else : 
        rank = "member" 
        rank_txt = "عضو 🙇‍♂️"
    c.execute("SELECT * FROM settings")
    pranks = c.fetchall()
    if rank == "member" :
        if ("contacts","locked") in pranks :
            bot.delete_message(cht_id,msg_id)
    conn.commit()
    conn.close()


@bot.message_handler(content_types=['location'])
def sticker_chk(message):
    id_num = message.from_user.id
    cht_id = message.chat.id
    msg_id = message.id
    conn = sqlite3.connect(f'{cht_id}.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    if id_num == sudo :
        rank = "main_dev"
        rank_txt = "المطور الأساسي 👨‍✈️🧳"
    elif id_num in dev :
        rank = "dev"
        rank_txt = "مطور 🧑‍💻"
    elif (id_num,"main_creator") in pranks :
        rank = "main_creator"
        rank_txt = "الملك 👑"
    elif (id_num,"creator") in pranks :
        rank = "creator"
        rank_txt = "نائب الملك 🧑🏼‍💼"
    elif (id_num,"boss") in pranks :
        rank = "boss"
        rank_txt = "أمير 💍"
    elif (id_num,"admin") in pranks :
        rank = "admin"
        rank_txt = "نائب الأمير 🧑🏼‍💼"
    elif (id_num,"special") in pranks :
        rank = "special"
        rank_txt = "مميز 🤩"
    else : 
        rank = "member" 
        rank_txt = "عضو 🙇‍♂️"
    c.execute("SELECT * FROM settings")
    pranks = c.fetchall()
    if rank == "member" :
        if ("locations","locked") in pranks :
            bot.delete_message(cht_id,msg_id)
    conn.commit()
    conn.close()


@bot.message_handler(content_types=['document'])
def sticker_chk(message):
    id_num = message.from_user.id
    cht_id = message.chat.id
    msg_id = message.id
    conn = sqlite3.connect(f'{cht_id}.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    if id_num == sudo :
        rank = "main_dev"
        rank_txt = "المطور الأساسي 👨‍✈️🧳"
    elif id_num in dev :
        rank = "dev"
        rank_txt = "مطور 🧑‍💻"
    elif (id_num,"main_creator") in pranks :
        rank = "main_creator"
        rank_txt = "الملك 👑"
    elif (id_num,"creator") in pranks :
        rank = "creator"
        rank_txt = "نائب الملك 🧑🏼‍💼"
    elif (id_num,"boss") in pranks :
        rank = "boss"
        rank_txt = "أمير 💍"
    elif (id_num,"admin") in pranks :
        rank = "admin"
        rank_txt = "نائب الأمير 🧑🏼‍💼"
    elif (id_num,"special") in pranks :
        rank = "special"
        rank_txt = "مميز 🤩"
    else : 
        rank = "member" 
        rank_txt = "عضو 🙇‍♂️"
    c.execute("SELECT * FROM settings")
    pranks = c.fetchall()
    if rank == "member" :
        if ("documents","locked") in pranks :
            bot.delete_message(cht_id,msg_id)
    conn.commit()
    conn.close()

@bot.message_handler(regexp='^close')
def cloiu(message):
    bot.send_message(message.chat.id, me)


@bot.message_handler(regexp="")
def main(message):
    first_name = message.from_user.first_name
    text = message.text
    username = message.from_user.username
    msg_id = message.id
    id_num = message.from_user.id
    cht_id = message.chat.id

    rank = chk_rank(cht_id, id_num)[0]
    rank_txt = chk_rank(cht_id, id_num)[1]

    if text == "التاريخ" or text == "الوقت":
        datime = time_json()
        brthdate = datime['date_meladi']
        hgrydate = datime['date_hijri']
        current_time = datetime.now().strftime("%I:%M %p")     
        wekday = datime['today_ar']
        bot.reply_to(message, f"‎‎‎‎\nا♕♕♕♕♕♕♕♕♕♕♕♕♕ا\n\n*الوقت الحالي    |*`{current_time}`\nاليوم                 *|{wekday}*\n*التاريخ الهجري  |*{hgrydate}\n*التاريخ الميلادي|*{brthdate}\n\nا♕♕♕♕♕♕♕♕♕♕♕♕♕ا\n‎‎‎",parse_mode="markdown")
    
    elif text == "ايدي" : 
        if message.from_user.username != None:
            username = message.from_user.username
        else:
            username = 'مجهول'
        id_text = f"♕♕♕♕♕♕♕♕♕♕♕♕♕♕\n*Name|* {first_name}\n*Username|* @{username}\n*User ID|* `{id_num}`\n*Rank|* {rank_txt}\n♕♕♕♕♕♕♕♕♕♕♕♕♕♕"
        try:
            profile_pic = bot.get_user_profile_photos(id_num,limit=1,offset=0).photos[0][0].file_id
            bot.send_photo(cht_id,profile_pic,id_text,msg_id,parse_mode="markdown")
        except IndexError:
            bot.reply_to(message, id_text, parse_mode="markdown")

    elif text == 'كشف':
        if message.reply_to_message :
            id_num = message.reply_to_message.from_user.id
            rank = chk_rank(cht_id, id_num)[0]
            rank_txt = chk_rank(cht_id, id_num)[1]

            if message.reply_to_message.from_user.username != None:
                username = message.reply_to_message.from_user.username
            else:
                username = 'مجهول'
            name = message.reply_to_message.from_user.first_name
            id_text = f"♕♕♕♕♕♕♕♕♕♕♕♕♕♕\n*Name|* {name}\n*Username|* @{username}\n*User ID|* `{id_num}`\n*Rank|* {rank_txt}\n♕♕♕♕♕♕♕♕♕♕♕♕♕♕"  
            try:
                profile = bot.get_user_profile_photos(id_num, limit=1, offset=0).photos[0][0].file_id
                bot.send_photo(message.chat.id, profile, id_text, message.id, parse_mode="markdown")
            except IndexError:
                bot.reply_to(message, id_text, parse_mode="markdown")

    elif text == "info" :
        if rank == "main_dev" or rank == "dev" :
            name = message.chat.title
            username = message.chat.username
            members_count = bot.get_chat_members_count(cht_id)
            admins_count = len(bot.get_chat_administrators(cht_id))
            photo = get(bot.get_file_url(bot.get_chat(cht_id).photo.big_file_id)).content
    
            owner_name = "None"
            owner_username = "None"
            owner_id = "None"

            for i in bot.get_chat_administrators(cht_id):
                if i.status == 'creator': 
                    owner_name = i.user.first_name
                    owner_username = i.user.username
                    owner_id = i.user.id

            text = f"♕♕♕♕♕♕♕♕♕♕♕♕♕♕\n*Name               |* {name}\n*Group ID         |* `{cht_id}`\n*Group User    |* @{username}\n*Member          |* {members_count}\n*Admins            |* {admins_count}\n*——————————————*\n*Owner Name |* {owner_name}\n*Owner ID        |* `{owner_id}`\n*Owner user    |* @{owner_username}\n♕♕♕♕♕♕♕♕♕♕♕♕♕♕"
            bot.send_photo(message.chat.id, photo, text, msg_id, parse_mode="markdown")  

print("Running...")
bot.polling()

