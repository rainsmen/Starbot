import logging
import global_vars
import json
import requests
import message_send

admin_id = global_vars.get_var('admin_id')
ws_url = global_vars.get_var('ws_url')
log_level = global_vars.get_var('log_level')
http_url = global_vars.get_var('http_url')

logging.basicConfig(level=log_level, format='[Star] %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def group_kick(ws, group_id, user_id, reject_add_request='false'):
    data = {
        'group_id': group_id,
        'user_id': user_id,
        'reject_add_request': reject_add_request
    }
    action = 'set_group_kick'
    post_data = json.dumps({'action': action, 'params': data})
    ws.send(post_data)


def group_single_ban(ws, group_id, user_id, duration):
    data = {
        'group_id': group_id,
        'user_id': user_id,
        'duration': duration
    }
    action = 'set_group_ban'
    post_data = json.dumps({'action': action, 'params': data})
    ws.send(post_data)


def group_whole_ban(ws, group_id, enable='true'):
    data = {
        'group_id': group_id,
        'enable': enable
    }
    action = 'set_group_whole_ban'
    post_data = json.dumps({'action': action, 'params': data})
    ws.send(post_data)


def set_group_admin(ws, group_id, user_id, enable='true'):
    data = {
        'group_id': group_id,
        'user_id': user_id,
        'enable': enable
    }
    action = 'set_group_admin'
    post_data = json.dumps({'action': action, 'params': data})
    ws.send(post_data)


def set_group_card(ws, group_id, user_id, card):
    data = {
        'group_id': group_id,
        'user_id': user_id,
        'card': card
    }
    action = 'set_group_card'
    post_data = json.dumps({'action': action, 'params': data})
    ws.send(post_data)


def set_group_name(ws, group_id, group_name):
    data = {
        'group_id': group_id,
        'group_name': group_name
    }
    action = 'set_group_name'
    post_data = json.dumps({'action': action, 'params': data})
    ws.send(post_data)


def set_group_special_title(ws, group_id, user_id, special_title, duration):
    data = {
        'group_id': group_id,
        'user_id': user_id,
        'special_title': special_title,
        'duration':duration
    }
    action = 'set_group_special_title'
    requests.get(http_url + action, params=data)


def upload_group_file(ws, group_id, file, name):
    data = {
        'group_id': group_id,
        'file': file,
        'name': name
    }
    action = 'upload_group_file'
    post_data = json.dumps({'action': action, 'params': data})
    ws.send(post_data)


def _send_group_notice(ws, group_id, content):
    data = {
        'group_id': group_id,
        'content': content
    }
    action = '_send_group_notice'
    post_data = json.dumps({'action': action, 'params': data})
    ws.send(post_data)


'''获取群文件列表信息部分，暂时咕了
def get_group_root_files(group_id):
    data = {
        'group_id': group_id
    }
    action = 'get_group_root_files'
    rev = json.loads(requests.get(http_url + action, params=data).text)
    return rev


def get_group_files_by_folder(group_id, folder_id):
    data = {
        'group_id': group_id,
        'folder_id': folder_id
    }
    action = 'get_group_files_by_folder'
    rev = json.loads(requests.get(http_url + action, params=data).text)
    return rev
'''


def main(ws, message):
    sliced_message = message['raw_message'].split('@$')
    print(sliced_message)
    if sliced_message[1] == '踢人':
        group_kick(ws, sliced_message[2], sliced_message[3], sliced_message[4])
    elif sliced_message[1] == '禁言':
        group_single_ban(ws, sliced_message[2], sliced_message[3], sliced_message[4])
    elif sliced_message[1] == '全员禁言':
        group_whole_ban(ws, sliced_message[2], sliced_message[3])
    elif sliced_message[1] == '设置管理员':
        set_group_admin(ws, sliced_message[2], sliced_message[3], sliced_message[4])
    elif sliced_message[1] == '设置群名片':
        set_group_card(ws, sliced_message[2], sliced_message[3], sliced_message[4])
    elif sliced_message[1] == '设置头衔':
        set_group_special_title(ws, sliced_message[2], sliced_message[3], sliced_message[4], sliced_message[5])
    elif sliced_message[1] == '上传群文件':
        upload_group_file(ws, sliced_message[2], sliced_message[3], sliced_message[4])
    elif sliced_message[1] == '发公告':
        _send_group_notice(ws, sliced_message[2], sliced_message[3])
    else:
        if message['message_type'] == 'group':
            message_send.send_message('您输入的指令有误，请检查后再次输入。', message['group_id'], message['sender']['user_id'], message['message_id'], ws, 'group', 1)
        elif message['message_type'] == 'private':
            message_send.send_message('您输入的指令有误，请检查后再次输入。', message['group_id'], message['sender']['user_id'], message['message_id'], ws, 'private', 1)
        else:
            log.error('Wrong input')
            pass
    pass
