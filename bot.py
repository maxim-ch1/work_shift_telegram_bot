# -*- coding: utf-8 with BOM -*-
import telebot
from datetime import datetime
import sqlite3
import time
import logging
from days_module import day_today
from days_module import day_tomorrow
from days_module import day_yesterday
from days_module import weeks
from days_module import next_week


logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO, filename="inf_log_bot.log")
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.ERROR , filename="err_log_bot.log")
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename = "deb_log_bot.log")

token = 'telegram_token'

bot = telebot.TeleBot(token)

logging.info('---Staring bot---')

bd = 'users_base.db'

#функция блокирует пользователей которым не одобрен доступ

def block_noname(tg_id):

    con = sqlite3.connect(bd)
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE id=:id', {'id': tg_id})
    lock = cur.fetchone()

    if lock == None:
        a = 0
    elif lock[1] == 1:
        a = 0
    else:
        a = 1

    return a

#После выполнения команды /start в таблицу Users добавляется строка с информацией
#о пользователе, при этом в стобце access добавляется 0. Это сделано для,
# того чтобы сторонние люди которые нашли бота, не смогли им воспользоваться

@bot.message_handler(commands=['start'])
def handle_start_help(message):

    logging.info('---BOT command /start---' + ' USER: ' + str(message.chat.username) + ' - ' + str(message.chat.id))

    bot.send_message(message.chat.id, 'Привет! Я OIT BOT. Я умею предоставлять информацию по расписнию. '
                                      'Для предоставления доступа к боту, требуется обратиться к администратору бота.')

    con = sqlite3.connect(bd)
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE id=:id', {'id': message.chat.id})

    try_id = cur.fetchone()

    telegram_users_ids = ((0, None, message.chat.id, message.chat.username, message.chat.first_name,
                           message.chat.last_name, datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M.%f")),)

    if try_id == None:
        cur.executemany("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", telegram_users_ids)
        con.commit()
        con.close()

    logging.info('---BOT command /start END---' + ' USER: ' + str(message.chat.username) + ' - ' + str(message.chat.id))

@bot.message_handler(commands=['yesterday'])
def today(message):

    tg_id = str(message.chat.id)
    tg_username = message.chat.username
    local_blocker = block_noname(tg_id)

    try:
        logging.info('---BOT command /yesterday---' + ' USER: ' + tg_username + ' - ' + tg_id)
        if local_blocker == 1:
            print('---yesterday---')
            bot.send_message(tg_id, day_yesterday())
        else:
            bot.send_message(tg_id, 'У тебя не хватает прав для использования этой функции.')
    except:
        logging.info(
            '---BOT command /yesterday (ERROR)---' + ' USER: ' + tg_username + ' - ' + str(
                tg_id))
        bot.send_message(tg_id, 'Упс, пошло что-то не так! ERR 1')

        logging.info('---BOT command /yesterday END---' + ' USER: ' + tg_username)

@bot.message_handler(commands=['today'])
def today(message):

    tg_id = str(message.chat.id)
    tg_username = message.chat.username
    local_blocker = block_noname(tg_id)

    try:
        logging.info('---BOT command /today---' + ' USER: ' + tg_username + ' - ' + tg_id)
        if local_blocker == 1:
            print('---today---')
            bot.send_message(tg_id, day_today())
        else:
            bot.send_message(tg_id, 'У тебя не хватает прав для использования этой функции.')
    except:
        logging.info(
            '---BOT command /today (ERROR)---' + ' USER: ' + tg_username + ' - ' + tg_id)
        bot.send_message(tg_id, 'Упс, пошло что-то не так! ERR 1')

@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):

    tg_id = str(message.chat.id)
    tg_username = message.chat.username
    local_blocker = block_noname(tg_id)

    try:
        logging.info('---BOT command /tomorrow---' + ' USER: ' + tg_username + ' - ' + tg_id)
        if local_blocker == 1:
            print('---tomorrow---')
            bot.send_message(tg_id, day_tomorrow())
        else:
            bot.send_message(tg_id, 'У тебя не хватает прав для использования этой функции.')
    except:
        logging.info('---BOT command /tomorrow (ERROR)---' + ' USER: ' + tg_username + ' - ' + tg_id)
        bot.send_message(tg_id, 'Упс, пошло что-то не так! ERR 2')

@bot.message_handler(commands=['week'])
def thisweek(message):

    tg_id = str(message.chat.id)
    tg_username = message.chat.username
    local_blocker = block_noname(tg_id)

    try:
        logging.info('---BOT command /week---' + ' USER: ' + tg_username + ' - ' + tg_id)
        if local_blocker == 1:
            print('---week---')
            bot.send_message(tg_id, weeks())
        else:
            bot.send_message(tg_id, 'У тебя не хватает прав для использования этой функции.')
    except:
        logging.info('---BOT command /week (ERROR)---' + ' USER: ' + tg_username + ' - ' + tg_id)
        bot.send_message(tg_id, 'Упс, пошло что-то не так! ERR 3')

@bot.message_handler(commands=['nextweek'])
def nextweek(message):

    tg_id = str(message.chat.id)
    tg_username = message.chat.username
    local_blocker = block_noname(tg_id)

    try:
        logging.info('---BOT command /nextweek---' +
                     ' USER: ' + str(message.chat.username) + ' - ' + str(message.chat.id))
        if local_blocker == 1:
            print('---nextweek---')
            bot.send_message(tg_id, next_week())
        else:
            bot.send_message(tg_id, 'У тебя не хватает прав для использования этой функции.')
    except:
        logging.info('---BOT command /nextweek (ERROR)---' +
                     ' USER: ' + tg_username + ' - ' + tg_id)
        bot.send_message(tg_id, 'Упс, пошло что-то не так! ERR 3')

while True:
    try:
        bot.polling(none_stop=True, timeout=30)
    except:
        logging.error(str(datetime.now()) + ':  бот упал')
        print('restart')
        time.sleep(10)