import json
import global_vars
import setu

reply_mode = global_vars.get_var('reply_mode')

special_list = [91]


def send_message(msg, qq_id, sender_id, msg_id, ws, qq_type, i):
    if msg == None:
        return False
    if qq_type == "private" and i not in special_list:
        if i == 1:
            data = {
                'user_id': qq_id,
                'message': msg,
                'auto_escape': False
            }
            action = "send_private_msg"
            post_data = json.dumps({"action": action, "params": data})
            print(post_data)
            rev = ws.send(post_data)
        elif i == 2:
            r_msg = ''
            i = 0
            while i < len(msg):
                r_msg = r_msg + msg[i] + '\n'
                i += 1
            data = {
                'user_id': qq_id,
                'message': '你是想说这些吗？\n' + r_msg,
                'auto_escape': False
            }
            action = "send_private_msg"
            post_data = json.dumps({"action": action, "params": data})
            rev = ws.send(post_data)
    elif qq_type == "group" and i not in special_list:
        if reply_mode == 'True':
            if i == 1:
                data = {
                    'group_id': qq_id,
                    'message': f'[CQ:reply,id={msg_id}]' + msg,
                    'auto_escape': False
                }
                action = "send_group_msg"
                post_data = json.dumps({"action": action, "params": data})
                rev = ws.send(post_data)
            elif i == 2:
                r_msg = ''
                i = 0
                while i < len(msg):
                    r_msg = r_msg + msg[i] + '\n'
                    i += 1
                data = {
                    'group_id': qq_id,
                    'message': f'[CQ:reply,id={msg_id}] 你是想说这些吗？\n' + r_msg,
                    'auto_escape': False
                }
                action = "send_group_msg"
                post_data = json.dumps({"action": action, "params": data})
                rev = ws.send(post_data)
            else:
                return False
        else:
            if i == 1:
                data = {
                    'group_id': qq_id,
                    'message': msg,
                    'auto_escape': False
                }
                action = "send_group_msg"
                post_data = json.dumps({"action": action, "params": data})
                rev = ws.send(post_data)
            elif i == 2:
                r_msg = ''
                i = 0
                while i < len(msg):
                    r_msg = r_msg + msg[i] + '\n'
                    i += 1
                data = {
                    'group_id': qq_id,
                    'message': '你是想说这些吗？\n' + r_msg,
                    'auto_escape': False
                }
                action = "send_group_msg"
                post_data = json.dumps({"action": action, "params": data})
                rev = ws.send(post_data)
            else:
                return False
    elif i == 91:
        if qq_type == 'group':
            file = setu.setu_geturl()
            message = f'[CQ:image,file=file:///{file}]\n{msg}'
            data = {
                'group_id': qq_id,
                'message': message,
            }
            action = "send_group_msg"
            post_data = json.dumps({"action": action, "params": data})
            rev = ws.send(post_data)
        elif qq_type == 'private':
            file = setu.setu_geturl()
            message = f'[CQ:image,file=file:///{file}]\n' + msg
            data = {
                'user_id': qq_id,
                'message': message,
            }
            action = "send_private_msg"
            post_data = json.dumps({"action": action, "params": data})
            rev = ws.send(post_data)
        else:
            return False
    else:
        return False
    # print(rev)
    if rev is None or rev['status'] == 'failed':
        return False
    else:
        # return ret['data']['message_id']
        # if json.loads(rev)['status'] == 'ok':
        return True
