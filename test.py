ranks_level = {'main_dev':7, 'dev':6, 'main_creator':5, 'creator':4, 'boss':3, 'admin':2, 'special':1, 'member':0}
ranks_trans = {'main_dev':'مطور اساسي', 'dev':'مطور', 'main_creator':'منشئ اساسي', 'creator':'منشئ', 'boss':'مدير', 'admin':'ادمن', 'special':'مميز', 'member':'عضو'}
level_ranks = {7:'main_dev', 6:'dev', 5:'main_creator', 4:'creator', 3:'boss', 2:'admin', 1:'special', 0:'member'}
ranks_text = {'main_dev':"المطور الأساسي 👨‍✈️🧳", 'dev':"مطور 🧑‍💻", 'main_creator':"الملك 👑", 'creator':"نائب الملك 🧑🏼‍💼", 'boss':"أمير 💍", 'admin':"نائب الأمير 🧑🏼‍💼", 'special':"مميز 🤩", 'member':"عضو 🙇‍♂️"}
ranks_text_ar = {"مطور اساسي":"المطور الأساسي 👨‍✈️🧳", "مطور":"مطور 🧑‍💻", "منشئ اساسي":"الملك 👑", "منشئ":"نائب الملك 🧑🏼‍💼", "مدير":"أمير 💍", "ادمن":"نائب الأمير 🧑🏼‍💼", "مميز":"مميز 🤩", "عضو":"عضو 🙇‍♂️"}

sudo = 1402010763
dev = [942683545,1207564961]

def max_rank(d):
      d_list = []
      if len(d) > 0:
            for i in d:
                  d_list.append(ranks_level[i])
            max_rank_num = max(d_list)
            return level_ranks[max_rank_num]
      else:
            return d


@bot.message_handler(regexp="^رفع")
def rnkUp(message):
      text = message.text.replace('رفع').strip()
      msg_id = message.id
      cht_id = message.chat.id
      caller_id = message.from_user.id
      target_id = message.reply_to.from_user.id

      conn = sqlite3.connect(f'{cht_id}.db')
      c = conn.cursor()

      c.execute(f"SELECT * FROM ranks WHERE id_num={caller_id}")
      caller_rank = c.fetchall()
      if len(caller_rank) > 0:
            caller_rank = max_rank(caller_rank)
      
      c.execute(f"SELECT * FROM ranks WHERE id_num={target_id}")
      target_rank = c.fetchall()
      if len(target_rank) > 0:
            target_rank = max_rank(target_rank)


      if ranks_level[ranks_trans[text]] >= 6:
            if caller_rank == "main_dev":
                  bot.reply_to(message,"You should add the developer manually🛠")
            else: 
                  bot.reply_to(message,"sorry but you don't have permission 😊")
      else:
            if ranks_level[ranks_trans[text]] >= 2:
                  if message.reply_to_message:
                        if ranks_level[caller_rank] > ranks_level[ranks_trans[text]]:
                              if target_rank != ranks_trans[text]:
                                    with conn:
                                          bot.reply_to(message, f"ا♕♕♕♕♕♕♕♕♕♕ا\n\nتمت ترقيته ليصبح {ranks_text_ar[text]} بواسطة {ranks_text[caller_rank]}\n\nا♕♕♕♕♕♕♕♕♕♕ا\n.")
                                          c.execute(f'INSERT INTO ranks VALUES ({int(target_id)}, {ranks_trans[text]}')
                                   
                              else:
                                    bot.reply_to(message,"هو بالفعل أمير😊")
                        else:
                              bot.reply_to(message,"sorry but you don't have permission 😊")     
                  else:
                        bot.send_message(message.chat.id,"who? 👀")
            else:
                  bot.reply_to(message,"sorry but you don't have permission 😊")


@bot.message_handler(regexp='^تنزيل')
def rnkDown(message):
      text = message.text.replace('رفع').strip()
      msg_id = message.id
      cht_id = message.chat.id
      caller_id = message.from_user.id


      conn = sqlite3.connect(f'{cht_id}.db')
      c = conn.cursor()

      c.execute(f"SELECT * FROM ranks WHERE id_num={caller_id}")
      caller_rank = c.fetchall()
      if len(caller_rank) > 0:
            caller_rank = max_rank(caller_rank)


      if ranks_level[ranks_trans[text]] >= 6:
            if caller_rank == "main_dev":
                  bot.reply_to(message,"You should edite the developer manually🛠")
            else: 
                  bot.reply_to(message,"sorry but you don't have permission 😊")
      else:
            if ranks_level[ranks_trans[text]] >= 2:
                  if message.reply_to_message:
                        target_id = message.reply_to.from_user.id
                        target_name = message.reply_to.from_user.first_name
                        c.execute(f"SELECT * FROM ranks WHERE id_num={target_id}")
                        target_rank = c.fetchall()

                        if ranks_level[caller_rank] > ranks_level[ranks_trans[text]]:
                              if len(target_rank) > 0:
                                    if ranks_trans[text] in target_rank:
                                          bot.reply_to(message, f"ا♕♕♕♕♕♕♕♕♕♕ا\n\n تم تنزيل {target_name} من رتبة {ranks_text[text]} بواسطة {ranks_text[caller_rank]}")
                                          c.execute(f'DELETE FROM ranks WHERE id_num={int(target_id)} AND rank={ranks_trans[text]}')
                                    else:
                                          bot.reply_to(message, f"هو بالفعل ليس {text} 😊")
                                          
                              else:
                                    if ranks_trans[text] == target_rank:
                                          bot.reply_to(message, f"ا♕♕♕♕♕♕♕♕♕♕ا\n\n تم تنزيل {target_name} من رتبة {ranks_text[text]} بواسطة {ranks_text[caller_rank]}")
                                          c.execute(f'DELETE FROM ranks WHERE id_num={int(target_id)} AND rank={ranks_trans[text]}')
                                    else:
                                          bot.reply_to(message, f"هو بالفعل ليس {text} 😊")

                        else:
                              bot.reply_to(message,"sorry but you don't have permission 😊")
                  else:
                        bot.send_message(message.chat.id,"who? 👀")
            else:
                  bot.reply_to(message,"sorry but you don't have permission 😊")
