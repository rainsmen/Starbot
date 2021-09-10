import logging
import json
import threading
import time
import websocket

import event_handle
import global_vars
import message_handle
from message_handle import *
jieba.set_dictionary("dict.txt")
jieba.initialize()

ws_url = global_vars.get_var('ws_url')
log_level = global_vars.get_var('log_level')
enabled_groups = global_vars.get_var('enabled_groups')
admin_id = global_vars.get_var('admin_id')
gr_admin_id = global_vars.get_var('gr_admin_id')
enabled_at = global_vars.get_var('enabled_at')
botqq = global_vars.get_var('botqq')

logging.basicConfig(level=log_level, format='[Star] %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def receive_message(_, message):
    try:
        j_message = json.loads(message)
        if j_message == None:
            return False
        else:
            # 消息事件
            if j_message['post_type'] == 'message':
                # 涩图发送（最高优先级
                if j_message['raw_message'] == 'setu':
                    message_handle.setu_(j_message, ws)
                elif '@$' in j_message['raw_message'] and str(j_message['sender']['user_id']) in gr_admin_id:
                    ths = []
                    x = threading.Thread(target=event_handle.main(ws, j_message))
                    ths.append(x)
                    while ths:
                        ths[-1].start()
                        ths.pop()
                # 群， 需要at机器人
                elif j_message['message_type'] == 'group' and str(j_message[
                'group_id']) in enabled_groups and enabled_at == 'True':
                    if f'[CQ:at,qq={botqq}' in j_message['raw_message']:
                        ths = []
                        x = threading.Thread(target=message_handle.main_at(j_message, ws))
                        ths.append(x)
                        while ths:
                            ths[-1].start()
                            ths.pop()
                    else:
                        pass
                # 群， 无需at机器人
                elif j_message['message_type'] == 'group' and str(j_message[
                'group_id']) in enabled_groups and enabled_at == 'False':
                    ths = []
                    x = threading.Thread(target=message_handle.main(j_message, ws))
                    ths.append(x)
                    while ths:
                        ths[-1].start()
                        ths.pop()
                # 私聊
                elif j_message['message_type'] == 'private':
                    # 普通用户
                    if str(j_message['sender']['user_id']) != admin_id:
                        ths = []
                        x = threading.Thread(target=message_handle.main(j_message, ws))
                        ths.append(x)
                        while ths:
                            ths[-1].start()
                            ths.pop()
                    # 管理员
                    elif str(j_message['sender']['user_id']) == admin_id:
                        slided = j_message['raw_message'].split('@#')
                        message_handle.learn(slided[0], slided[1], ws)
                else:
                    pass
            # 通知事件
            elif j_message['post_type'] == 'notice':
                log.info(message)
            # 心跳等go-cqhttp内置事件
            elif j_message['post_type'] == 'meta_event':
                log.info(message)
            else:
                log.warning('未知事件类型')
    except Exception as e:
        log.error(e)


if __name__ == '__main__':
    ws = websocket.WebSocketApp(
        ws_url,
        on_message=receive_message,
        on_open=lambda _: log.info('连接成功'),
        on_close=lambda _: log.warning('重连中......'),
    )
    while True:
        ws.run_forever()
        time.sleep(5)
