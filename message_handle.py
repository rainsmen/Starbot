import threading
import time
import sqlite3
import jieba
jieba.set_dictionary("dict.txt")
jieba.initialize()

import jieba.analyse
import logging
import global_vars
import message_send

admin_id = global_vars.get_var('admin_id')
log_level = global_vars.get_var('log_level')
botqq = global_vars.get_var('botqq')
database_url = global_vars.get_var('database_url')

logging.basicConfig(level=log_level, format='[Star] %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)




def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect(database_url)
db.row_factory = dict_factory
cur = db.cursor()


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            log.error(e)


def select(message):
    # execute方式执行查询语句
    db_s = f'select * from q_and_a where quz = \'{message}\' or id = \'{message}\''
    cur.execute(db_s)
    results = cur.fetchone()
    # print(db_s)
    if results:
        log.info('全字匹配到结果')
        return results
    else:
        log.info('全字匹配为空')
        return False


def like_select(message):
    # execute方式执行查询语句
    cur.execute(f'select * from q_and_a where quz like \'%{message}%\'')
    results = cur.fetchone()
    if results:
        log.info('模糊匹配到结果')
        return results
    else:
        log.info('模糊匹配为空')
        return False


def keyword_like_select(message):
    keywords = jieba.analyse.extract_tags(message, topK=5, allowPOS=('n', 'v'))
    if len(keywords) < 2:
        log.info('关键字不足')
        return False
    else:
        dbselect = f'select * from q_and_a where quz like \'%{keywords.pop()}%\' '
        for word in keywords:
            dbselect += f'and quz like\'%{word}%\' '
        cur.execute(dbselect)
        results = cur.fetchall()
        # print(dbselect)
        if results:
            log.info('关键字匹配到结果')
            return results
        else:
            log.info('关键字匹配为空')
            return False


def learn(quz, ans, ws):
    # execute方式执行语句
    cur.execute(f'insert into q_and_a(quz,ans) values(\'{quz}\',\'{ans}\')')
    db.commit()
    message_send.send_message(quz+'\n'+ans, admin_id, None, None, ws, 'private', i=1)


def main_at(message, ws):
    ths = []
    result = []
    # 切除前部at机器人的CQ码
    str = list(message['raw_message'])
    str = ''.join(str)
    length = 12 + len(botqq)
    sliced_message = str.replace(message['raw_message'][0:length + 0:1], '')

    select_ways = [select, like_select, keyword_like_select]

    for i in select_ways:
        print(sliced_message)
        x = MyThread(i, args=(sliced_message,))
        ths.append(x)
    '''while length < len(ths):
        ths[-1].start()
        print('started ', ths[-1])
        length += 1
    for t in ths:
        t.join()'''
    for t in ths:
        result.append(t.get_result())
    if message['message_type'] == 'group':
        if result[0]:
            log.info('全字匹配回复')
            message_send.send_message(result[0]['ans'], message['group_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'group', i=1)
        elif result[1]:
            log.info('模糊匹配回复')
            message_send.send_message(result[1][0]['quz'], message['group_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'group', i=2)
            time.sleep(0.5)
            message_send.send_message(result[1][0]['ans'], message['group_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'group', i=1)
        elif result[2]:
            log.info('关键字匹配回复')
            quz = []
            i = 0
            while i < len(result[2]):
                quz.append(result[2][i]['quz'])
                i += 1
            message_send.send_message(quz, message['group_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'group', i=2)
        else:
            return False


def main(message, ws):
    ths = []
    result = []

    select_ways = [select, like_select, keyword_like_select]

    for i in select_ways:
        x = MyThread(i, args=(message['raw_message'],))
        ths.append(x)
    '''while length < len(ths):
        ths[-1].start()
        print('started ', ths[-1])
        length += 1
    for t in ths:
        t.join()'''
    for t in ths:
        result.append(t.get_result())
    if message['message_type'] == 'group':
        if result[0]:
            log.info('全字匹配回复')
            message_send.send_message(result[0]['ans'], message['group_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'group', 1)
        elif result[1]:
            log.info('模糊匹配回复')
            message_send.send_message(result[1]['ans'], message['group_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'group', 1)
        elif result[2]:
            log.info('关键字匹配回复')
            quz = []
            i = 0
            while i < len(result[2]):
                quz.append(result[2][i]['quz'])
                i += 1
            message_send.send_message(quz, message['group_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'group', 2)
        else:
            return False
    elif message['message_type'] == 'private':
        if result[0]:
            log.info('全字匹配回复')
            message_send.send_message(result[0]['ans'], message['user_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'private', 1)
        elif result[1]:
            log.info('模糊匹配回复')
            message_send.send_message(result[1]['ans'], message['user_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'private', 1)
        elif result[2]:
            log.info('关键字匹配回复')
            quz = []
            i = 0
            while i < len(result[2]):
                quz.append(result[2][i]['quz'])
                i += 1
            message_send.send_message(quz, message['user_id'], message['sender']['user_id'],
                                      message['message_id'], ws, 'private', 2)
        else:
            return False


def setu_(message, ws):
    t = '色狗！kimo！'
    if message['message_type'] == 'group':
        message_send.send_message(t, message['group_id'], message['sender']['user_id'],
                                  message['message_id'], ws, 'group', 91)
    elif message['message_type'] == 'private':
        message_send.send_message(t, message['user_id'], message['sender']['user_id'],
                                  message['message_id'], ws, 'private', 91)
    else:
        return False
