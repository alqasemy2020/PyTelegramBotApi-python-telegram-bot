from templates import *
from bs4 import BeautifulSoup
from datetime import datetime
import telebot
import sqlite3
import pytz
from text import user_data
from threading import Thread
import asyncio
import json
from time import sleep, time
import aiohttp
from aiohttp import ClientSession
import requests
from telegram.ext import Updater, Filters
from telegram.chatpermissions import ChatPermissions
from os import remove, mkdir, path, listdir, removedirs
from secrets import choice, token_hex
from PIL import Image, ImageDraw
from io import BytesIO

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


TOKEN = "1654109240:AAHNYRyKZJTJjpikeBCng40XTm9t8oVtTmw"
bot = telebot.TeleBot(TOKEN)
sudo = 1405097902
dev  = [942683545, 1207564961]
dev.append(sudo)


# ------------------- DATABASE -------------------------
conn = sqlite3.connect('DARK.db')
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS ranks (
    id_num intger ,
    rank text)""")

c.execute('CREATE TABLE IF NOT EXISTS activating (is_activating bool)')
for i in dev:
    if i == sudo:
        __rank = 'main_dev'
    else:
        __rank = 'dev'
    c.execute('SELECT * FROM ranks')
    pr = c.fetchall()
    if (i, __rank) in pr:
        pass
    else:
        c.execute(f'INSERT INTO ranks VALUES ({i}, "{__rank}")')
    conn.commit()

c.execute('SELECT * FROM ranks')
print(c.fetchall())
conn.close()


ranks_level = {'main_dev':7, 'dev':6, 'main_creator':5, 'creator':4, 'boss':3, 'admin':2, 'special':1, 'member':0}
ranks_trans_en2ar = {'main_dev':'مطور اساسي', 'dev':'مطور', 'main_creator':'منشئ اساسي', 'creator':'منشئ', 'boss':'مدير', 'admin':'ادمن', 'special':'مميز', 'member':'عضو'}
ranks_trans = {'مطور اساسي':'main_dev', 'مطور':'dev', 'منشئ اساسي':'main_creator', 'منشئ':'creator', 'مدير':'boss', 'ادمن':'admin', 'مميز':'special', 'عضو':'member'}
level_ranks = {7:'main_dev', 6:'dev', 5:'main_creator', 4:'creator', 3:'boss', 2:'admin', 1:'special', 0:'member'}
ranks_text = {'main_dev':"المطور الأساسي 👨‍✈️🧳", 'dev':"مطور 🧑‍💻", 'main_creator':"الملك 👑", 'creator':"نائب الملك 🧑🏼‍💼", 'boss':"أمير 💍", 'admin':"نائب الأمير 🧑🏼‍💼", 'special':"مميز 🤩", 'member':"عضو 🙇‍♂️"}
ranks_text_ar = {"مطور اساسي":"المطور الأساسي 👨‍✈️🧳", "مطور":"مطور 🧑‍💻", "منشئ اساسي":"الملك 👑", "منشئ":"نائب الملك 🧑🏼‍💼", "مدير":"أمير 💍", "ادمن":"نائب الأمير 🧑🏼‍💼", "مميز":"مميز 🤩", "عضو":"عضو 🙇‍♂️"}


def who_can_access(text):
    rank_n = ranks_level[ranks_trans[text]]
    who_can = '{'
    decore = '، '
    for i in ranks_level:
        if rank_n < ranks_level[i]:
            who_can = who_can + ranks_text[i] + decore
    return who_can[:-2] + '}'



# ------------------- DATABASE -------------------------
# ------------------- Activating Bot -------------------

@bot.message_handler(regexp='^تفعيل')
def activating_bot(message):
    devs = '@Yloxr'
    try:
        res = int(sqlite.read_all('activating'))
    except TypeError:
        try:
            res = int(sqlite.read_all('activating')[0])
        except IndexError:
            res = 0

    if res == 0:
        if message.from_user.id in dev:
            sqlite.insert('activating', '(True)')
            bot.reply_to(message, f"تم تفعيل البوت من قبل {message.from_user.first_name}")
            for i in dev:
                sqlite.insert('ranks', (i[0], i[2], i[3]))
        else:
            bot.reply_to(message, f'لاتمتلك الصلاحيات لتفعيل البت الرجاء التواصل مع المطورين {devs}')
    else:
        bot.reply_to(message, 'البوت بالفعل مفعل ،،،')


def is_actv():
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute('SELECT * FROM activating')
    sql = c.fetchall()

    if len(sql) > 0:
        res = int(sql[0][0])

        if res == 0:
            return False
        else:
            return True
    else:
        return False

# ------------- Activating Ends -------------------


@bot.message_handler(regexp='^fu')
def mljoi(message):
        id_num = message.chat.id
        admins = bot.get_chat_administrators(id_num)
        creators_list = 'creators: '
        admins_list = 'admins: '
        for i in admins:
            if i.user.username != None:
                username = '@' + i.user.username
            else:
                username = 'لايوجد'

            if i.status == 'administrator':
                admins_list = admins_list + str([i.user.first_name, i.user.id, username]) + ', '
            else:
                creators_list = creators_list + str([i.user.first_name, i.user.id, username]) + ', '


        bot.send_message(message.chat.id, creators_list +'\n'+ admins_list)
    # else:
        # bot.reply_to(message, 'bot isn\'t activating')

#-------------------- Ranks Starts ----------------------


def max_rank(d):
    d_list = []
    if len(d) > 1 and type(d) == list():
        for i in d:

            d_list.append(ranks_level[i[-1]])
        max_rank_num = max(d_list)
        return level_ranks[max_rank_num]
    else:
        if type(d) == str():
            return d
        else:
            return d[-1]


@bot.message_handler(regexp="^رفع")
def rnkUp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()

    msg_id = message.id
    cht_id = message.chat.id
    caller_id = message.from_user.id

    c.execute(f"SELECT * FROM ranks WHERE id_num={caller_id}")
    caller_rank = c.fetchall()
    run = True

    if len(caller_rank) >= 1:
        caller_rank = max_rank(caller_rank)
    else:
        caller_rank = 'member'

    try:
        text = message.text.replace('رفع', '').strip()
        who_can = who_can_access(text)

        if text != 'عضو':
            if ranks_level[ranks_trans[text]] >= 6:
                if caller_rank == "main_dev":
                        bot.reply_to(message,"You should add the developer manually🛠")
                else: 
                    bot.reply_to(message, f"هذا الامر يخص المطور الاساسي فقط، انت {ranks_text[caller_rank]}")
            else:
                if message.reply_to_message:
                    target_id = message.reply_to_message.from_user.id
                    c.execute(f"SELECT * FROM ranks WHERE id_num={target_id}")
                    target_rank = c.fetchall()

                    if len(target_rank) > 0:
                        target_rank = max_rank(target_rank)

                    if ranks_level[caller_rank] > ranks_level[ranks_trans[text]]:
                        if target_rank != ranks_trans[text]:
                            if ranks_level[ranks_trans[text]] != 0:
                                with conn:
                                        bot.reply_to(message, f"ا♕♕♕♕♕♕♕♕♕♕ا\n\nتمت ترقيته ليصبح {ranks_text_ar[text]} بواسطة {ranks_text[caller_rank]}\n\nا♕♕♕♕♕♕♕♕♕♕ا\n.")
                                        c.execute(f'INSERT INTO ranks VALUES ({int(target_id)}, "{ranks_trans[text]}")')
                                
                            else:
                                bot.reply_to(message, f"هو بالفعل {ranks_text_ar[text]}")
                        else:
                            bot.reply_to(message, f"هو بالفعل {ranks_text_ar[text]}")
                    else:
                        bot.reply_to(message,f"هذا الامر يخص {who_can} فقط، انت {ranks_text[caller_rank]}")  
                else:
                    bot.send_message(message.chat.id,"who? 👀")

    except KeyError:
        pass
    except TypeError:
        bot.reply_to(message,"sorry but you don't have permission 😊 TypeError") 




@bot.message_handler(regexp='^تنزيل')
def rnkDown(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()

    msg_id = message.id
    cht_id = message.chat.id
    caller_id = message.from_user.id

    c.execute(f"SELECT * FROM ranks WHERE id_num={caller_id}")
    caller_rank = c.fetchall()
    if len(caller_rank) >= 1:
        caller_rank = max_rank(caller_rank)
    else:
        caller_rank = 'member'

    try:
        text = message.text.replace('تنزيل', '').strip()
        who_can = who_can_access(text)

        if 'عضو' not in text:
            if ranks_level[ranks_trans[text]] >= 6:
                if caller_rank == "main_dev":
                    bot.reply_to(message,"You should edite the developer manually🛠")
                else: 
                    bot.reply_to(message, f"هذا الامر يخص المطور الاساسي فقط، انت {ranks_text[caller_rank]}")
            else:
                if message.reply_to_message:
                    target_id = message.reply_to_message.from_user.id
                    target_name = message.reply_to_message.from_user.first_name
                    c.execute(f"SELECT * FROM ranks WHERE id_num={target_id}")
                    target_rank = c.fetchall()

                    if ranks_level[caller_rank] > ranks_level[ranks_trans[text]]:
                            if len(target_rank) > 0:
                                if (target_id, ranks_trans[text]) in target_rank:
                                    bot.reply_to(message, f"ا♕♕♕♕♕♕♕♕♕♕ا\n\n تم تنزيل {target_name} من رتبة {ranks_text_ar[text]} بواسطة {ranks_text[caller_rank]}")
                                    c.execute(f'DELETE FROM ranks WHERE id_num={int(target_id)} AND rank="{ranks_trans[text]}"')
                                else:
                                    bot.reply_to(message, f"هو بالفعل ليس {text} 😊")
                            else:
                                if (target_id, ranks_trans[text]) in target_rank:
                                    bot.reply_to(message, f"ا♕♕♕♕♕♕♕♕♕♕ا\n\n تم تنزيل {target_name} من رتبة {ranks_text[text]} بواسطة {ranks_text[caller_rank]}")
                                    c.execute(f'DELETE FROM ranks WHERE id_num={int(target_id)} AND rank="{ranks_trans[text]}"')
                                else:
                                    bot.reply_to(message, f"هو بالفعل ليس {text} 😊")

                    else:
                        bot.reply_to(message,f"هذا الامر يخص {who_can} فقط، انت {ranks_text[caller_rank]}")
                else:
                    bot.send_message(message.chat.id,"who? 👀")
        else:
            pass

    except KeyError:
        pass
    except TypeError:
        bot.reply_to(message, "sorry but you don't have permission 😊")

    conn.commit()
# ----------------------- Ranks Ends ---------------------------



async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await session.request(method="GET", url=url, **kwargs)

async def make_requests(url: str, message_id, n, **kwargs) -> None:
    try:
        async with ClientSession() as session:
            tasks = []
            for i in range(1,n):
                tasks.append(
                    fetch_html(url=f'{url}{message_id - (int(n) - int(i))}', session=session, **kwargs)
                )
            results = await asyncio.gather(*tasks)
    except RuntimeError:
        pass


@bot.message_handler(regexp="^ايدي")# -------- MYID COMMAND
def idresp(message):
    start = time()
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()

    caller_id = message.from_user.id
    c.execute(f"SELECT * FROM ranks WHERE id_num={caller_id}")

    ranks = ''
    rank_data = c.fetchall()

    if len(rank_data) > 0:
        for i in rank_data:
            ranks = ranks + ranks_text[i[-1]] + '\n'
    else:
        ranks = ranks_text_ar['عضو']

    chtid_num = message.chat.id
    if message.from_user.username != None:
        username = message.from_user.username
    else:
        username = 'None'

    id_num = caller_id
    name = message.from_user.first_name
    try:
        profile = bot.get_user_profile_photos(id_num, limit=1, offset=0).photos[0][0].file_id
        bot.send_photo(message.chat.id, profile, user_data(name, id_num, username, ranks), message.id, parse_mode="markdown")
    except IndexError:
        bot.reply_to(message, user_data(name, id_num, username, ranks), parse_mode="markdown")

    print(time() - start)


@bot.message_handler(regexp="^كشف")# -------- MYID COMMAND
def idresp(message):

    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    chat_id = message.chat.id
    start = time()
    if message.reply_to_message:
        caller_id = message.from_user.id
        c.execute(f"SELECT * FROM ranks WHERE id_num={caller_id}")
        caller_rank = c.fetchall()
        if len(caller_rank) >= 1:
            caller_rank = max_rank(caller_rank)
        else:
            caller_rank = 'member'



        if ranks_level[max_rank(caller_rank)] >= 2:
            name = message.reply_to_message.from_user.first_name
            target_id = message.reply_to_message.from_user.id
            c.execute(f"SELECT * FROM ranks WHERE id_num={target_id}")
            target_ranks = c.fetchall()

            text_ranks = ''
            decore = '، '
            if len(target_ranks) > 0:
                for i in target_ranks:
                    if i == target_ranks[-1]:
                        decore = ''
                    text_ranks = text_ranks + ranks_text[i[-1]] + decore
            else:
                text_ranks = ranks_text_ar['عضو']

            if message.from_user.username != None:
                username = f'@{message.from_user.username}'
            else:
                username = 'None'

            try:
                profile = bot.get_user_profile_photos(target_id, limit=1, offset=0).photos[0][0].file_id
                bot.send_photo(chat_id, profile, user_data(name, target_id, username, text_ranks), message.id, parse_mode="markdown")
            except IndexError:
                bot.reply_to(message, user_data(name, target_id, username, text_ranks), parse_mode="markdown")

        else:
            bot.reply_to(message,"sorry but you don't have permission 😊")
    print(time() - start)



@bot.message_handler(regexp="^كفش")# -------- MYID COMMAND
def idresp(message):
    start = time()
    bot.reply_to(message, f'Sorry, but you don\'t have permission 😊{message.from_user.id}')
    print(time() - start)



@bot.message_handler(regexp="^date")  #-------- DATE AND TIME
@bot.message_handler(regexp="^التاريخ")  #-------- DATE AND TIME
@bot.message_handler(regexp="^تاريخ")  #-------- DATE AND TIME
def dateresp(message):
    start = time()
    if message.text.lower() == 'date' or 'التاريخ' or 'تاريخ':

        datime = time_json()
        brthdate = datime['date_meladi']
        hgrydate = datime['date_hijri']
        current_time = datetime.now().strftime("%I : %M  %p")
        wekday = datime['today_ar']

        # bot.reply_to(message, f"⏰ الوقت:{current_time} \n📅التاريخ الميلادي : {brthdate}\n🗓التاريخ الهجري : {hgrydate} {wekday}\n.")
        bot.reply_to(message, f"⏰ الوقت:{current_time} \n📅التاريخ الميلادي : {brthdate}\n🗓التاريخ الهجري : {hgrydate} {wekday}\n.") 

    print(time() - start)


@bot.message_handler(regexp='^رياكشن')
def send_reactions(message):
        category = message.text.split('رياكشن')[-1]
        if category.startswith(' '):
            category = category[1:]
        elif category.endswith(' '):
            category = category[0:-1]

        cht_id = message.chat.id 
        url = scrap_reactions(category)

        bot.send_animation(chat_id=cht_id, animation=url)


@bot.message_handler(regexp='^youtube')
def wds(message):
        pass


@bot.message_handler(regexp='^pin')
@bot.message_handler(regexp='^تثبيت')
def pin_msg(message):
        if message.reply_to_message:
            bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
            

@bot.message_handler(regexp='^حذف')
@bot.message_handler(regexp='^مسح')
def msg_del(message):
    # TODO! make an if statment to check weather the user was an admin or bigger if yes then deletes.
        try:
            if len(message.text) <= 4:
                if message.reply_to_message:
                    bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                else:
                    bot.delete_message(message.chat.id, message_id)
            else:
                chat_id = message.chat.id
                message_id = message.message_id
                try:
                    n = int(message.text.split('مسح ')[-1])
                    url = f'https://api.telegram.org/bot{TOKEN}/deleteMessage?chat_id={chat_id}&message_id='
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(make_requests(url=url, message_id=message_id, n=n))

                except ValueError:
                    bot.reply_to(message, 'valueError')
        except Exception:
            pass


@bot.message_handler(regexp='^close')
def boot_bot(message):
    print(message.from_user.id)
    if message.from_user.id == sudo:
        bot.send_message(message.chat.id, meow)


@bot.message_handler(content_types=['sticker'])
def del_s(message):
        if message.sticker != None:
            chat_id = message.chat.id
            message_id = message.id
            url = f'https://api.telegram.org/bot{TOKEN}/deleteMessage?chat_id={chat_id}&message_id={message_id}'
            res = requests.get(url)
        else:
            pass


# bot.restrict_chat_member(-1001346894503, 942683545, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_send_polls=False)


@bot.message_handler(regexp='^info')
def send_info(message):
    cht_id = message.chat.id
    name = message.chat.title
    msg_id = message.message_id
    username = message.chat.username
    members_count = bot.get_chat_members_count(cht_id)
    admins_count = len(bot.get_chat_administrators(cht_id))

    photoB = get(bot.get_file_url(bot.get_chat(cht_id).photo.big_file_id)).content
    start = time()
    photoB = Image.open(BytesIO(photoB))

    image = photoB.resize((640, 640), Image.ANTIALIAS)
    photo = BytesIO()
    image.save(photo, format="JPEG", optimize=True, quality=17  )
    photo = Image.open(photo)
    # red, green, blue = image.split()
    # photo = Image.merge("RGB", (green, red, blue))

    print(time() - start)


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



@bot.message_handler(regexp='^تقييد')
def set_delay(message):
        caller_id = message.from_user.id
        # caller_rank = sqlite.get_rank_by_id(caller_id)
        # if len(caller_rank) == 0:
        #     caller_rank = 'member'
        # else:
        #     caller_rank = caller_rank[0]

        # if caller_id == sudo or caller_id in dev or ranks_levels[caller_rank] >= ranks_levels['admin']:
        date = message.text.replace('تقييد', '').strip()
        run = True
        if 'د' in date:
            date = int(date.replace('د', '').strip())
            time_to_band = date * 60
        elif 'س' in date:
            date = int(date.replace('س', '').strip())
            time_to_band = date * 60 * 60
        elif 'ث' in date:
            date = float(date.replace('ث', '').strip())
            if int(date) <= 29:
                time_to_band = 35
            else:
                time_to_band = date
        else:
            bot.send_message(message.chat.id, 'wrong format')
            run= False

        if run == True:
            if message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
                chat_id = message.chat.id
        
                bandTime = time.time() + time_to_band
                try:
                    bot.restrict_chat_member(chat_id, user_id, until_date=bandTime, can_send_messages=False)
                    bot.reply_to(message, f'تم التقييد ل {int(time_to_band)} ')
                except Exception:
                    bot.reply_to(message, 'لا يمكنك تقييد المشرفين او منشئي القروب')

                # can_send_other_msesages for stickers and GIF
                # bot.reply_to(message, message.reply_to_message.from_user.id)
                # bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=False))
                # Thread(ktm(time_to_band, user_id, message.chat.id)).start()
                # bot.set_chat_administrator_custom_title(message.chat.id, message.reply_to_message.from_user.id, 'modeer')
                # print(bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, custom_title='modeer'))

    # else:
    #     bot.send_message(message.chat.id, f'لاتمتلك الصلاحيه لتقييد {message.reply_to_message.from_user.first_name}')

@bot.message_handler(regexp='^فك التقييد')
@bot.message_handler(regexp='^فك تقييد')
def set_delay(message):
    if message.reply_to_message:
        bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=True)
    else:
        bot.reply_to(message, 'نفك مين؟؟')



#####################Lists commands#####################
@bot.message_handler(regexp="^الاوامر")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.commands_list)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^م1")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M1)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^م2")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M2)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^م3")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M3)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^م4")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M4)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^م5")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M5)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^م6")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M6)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^م7")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M7)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^م المطور")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M_developer)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^اوامر الرد")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M_Reply)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^الوسائط")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M_Media)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^الاعدادات")  
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M_Settings)
    else: bot.reply_to(message,"وش تبي؟!!")

@bot.message_handler(regexp="^المطورين")
def comresp(message):
    conn = sqlite3.connect('DARK.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ranks")
    pranks = c.fetchall()
    id_num = message.from_user.id
    cht_id = message.chat.id
    if id_num == sudo or (id_num,'dev') in pranks or (id_num,cht_id,'main_creator') in pranks or (id_num,cht_id,'creator') in pranks or (id_num,cht_id,'boss') in pranks or (id_num,cht_id,'admin') in pranks:
        bot.reply_to(message,text.M_Developers)
    else: bot.reply_to(message,"وش تبي؟!!")
#####################Lists commands#####################



print ("Running ...")
bot.polling()

