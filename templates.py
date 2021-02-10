from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from pytz import timezone
from random import choice


class Rank():
    def __init__(self, id_num, chat_id, rank):
        self.id_num = id_num
        self.chat_id = chat_id
        self.rank = rank

    def __repr__(self):
        return "Rank('{}', '{}', '{}')".format(self.id_num, self.chat_id, self.rank) # {'id':self.id_, 'name':self.name, 'rank':self.rank}


class Editor():
    def __init__(self, conn, c):
        self.conn = conn
        self.c = c

    def read_all(self, table):
        self.c.execute(f'SELECT * FROM {table}')
        return self.c.fetchall()


    def search(self, table, data):
        self.c.execute(f'SELECT * FROM {table} WHERE {data}')
        return self.c.fetchall()


    def get_rank_by_id(self,id_):
        self.c.execute(f'SELECT * FROM rank WHERE id=:id', {'id': id_})
        return self.c.fetchall()


    def write(self, table, data):
        with self.conn:
            self.c.execute(f'INSERT INTO {table} VALUES (:id_num, :chat_id, :rank)', {'id_num': data.id_num, 'chat_id':data.chat_id, 'rank':data.rank})


    def update_rank(self, id_, new_rank):
        with self.conn:
            self.c.execute(f'UPDATE ranks SET rank="{new_rank}" WHERE id_num=:id', {'id': id_})


    def delete_user(self, table, id_, rank):
        with self.conn:
            self.c.execute(f'DELETE from ranks WHERE id_num={id_} AND rank="{rank}"')


class sqliteE():
    def __init__(self, conn, c):
        self.conn = conn
        self.c = c

    def execute(self, data):
        """formal executing function that just execute the data parametr"""
        with self.conn:
            self.c.execute(data)
    
    def dleete_rank(self, id_num, rank):
        with self.conn:
            self.c.execute(f'DELETE FROM ranks WHERE id_num={id_num} AND rank="{rank}"')

    def read_all(self, table):
        with self.conn:
            self.c.execute(f'SELECT * FROM {table}')
        return self.c.fetchall()

    def insert(self, table, data):
        """insert data like (7989, -17654356, "dev")"""
        with self.conn:
            self.c.execute(f'INSERT INTO {table} VALUES {data}')    

    def get_rank_by_id(self,id_):
        self.c.execute(f'SELECT * FROM ranks WHERE id_num=:id', {'id': id_})
        return self.c.fetchall()

    def get_pdf_by_chat_id(self,id_, n):
        self.c.execute(f'SELECT * FROM pdf WHERE chat_id={id_} AND img_num={n}')
        return self.c.fetchall()



def get_ranks(data):
    if len(data) == 0:
        return 'member'
    else:
        returned_data = []
        for field in data:
            returned_data.append(field[-1])

        return returned_



reactions = {
    'clapping': ['https://www.reactiongifs.us/wp-content/uploads/2019/01/Well-Done-Applause.gif', 'https://www.reactiongifs.us/wp-content/uploads/2018/07/Wake-Up-Applause.gif', 'https://www.reactiongifs.us/wp-content/uploads/2017/12/ezgif.com-optimize-2-1.gif'],
    'laugh': ['https://www.reactiongifs.us/wp-content/uploads/2014/11/lol_spider-man.gif', 'https://www.reactiongifs.us/wp-content/uploads/2018/01/very-funny.gif', 'https://www.reactiongifs.us/wp-content/uploads/2019/03/Will-Ferrell-LOL.gif'],
    'nice': ['https://www.reactiongifs.us/wp-content/uploads/2018/10/Nice.gif', 'https://www.reactiongifs.us/wp-content/uploads/2017/10/TAU-Nice.gif', ],
    'thank': ['https://www.reactiongifs.us/wp-content/uploads/2018/05/giphy-6.gif', 'https://www.reactiongifs.us/wp-content/uploads/2019/03/Thank-U.gif', 'https://www.reactiongifs.us/wp-content/uploads/2018/09/Thank-u.gif'],
    'no_one_care': ['https://www.reactiongifs.us/wp-content/uploads/2018/10/Tim-Meadows.gif'],
    'hmm': 'https://www.reactiongifs.us/wp-content/uploads/2019/02/Angry-Ace-Ventura.gif'}

reac_ar = {
    'clapping':['تصفيق', 'صفقه', 'clapping'],
    'laugh': ['ضحك', 'اضحاك', 'laugh', 'funny', 'إضحاك'],
    'thank': ['شكرا', 'thanks', 'thank', 'مشكور', 'تشكراتي', 'شكراً'],
    'nice': ['رائع', 'maboy', 'good', 'ممتاز', 'nice', 'حلو'],
    'no_one_care': ['no_one_care', 'ماحد يهتم', 'محد مهتم'],
    'hmm': ['hmm']}




def time_json():
    content = get('https://hijri-calendar.com/').content.decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    date_hijri = soup.find(class_='today').find(class_='hijri').text
    today_ar = soup.find(class_='today').find(class_='meladi').text
    date_meladi = soup.find(class_='today').find_all(class_='meladi')[-1].text
    today_en = datetime.now(timezone('Asia/Riyadh')).strftime('%a')
    return {'date_hijri':date_hijri, 'date_meladi':date_meladi, 'today_ar':today_ar, 'today_en': today_en}


def scrap_reactions(category):
    re = 'hmm'
    for i in reactions:
        da = reac_ar[i]
        for sin in da:
            if sin == category:
                re = i
                break

    urls = reactions[re]
    if type(urls) == list:
        url = choice(urls)

    else:
        url = urls

    return url

