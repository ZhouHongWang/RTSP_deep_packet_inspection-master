#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
from scapy.all import *
from rtsphandle.rtsp import *
from include.db import *
import datetime
import json

CRLF = "\r\n"
#RTSP协议指纹
RTSP_fingerprints=[
    "DESCRIBE",
    "ANNOUNCE",
    "GET_PARAMETER",
    "OPTIONS",
    "PAUSE",
    "PLAY",
    "RECORD",
    "REDIRECT",
    "SETUP",
    "SET_PARAMETER",
    "TEARDOWN",
    "RTSP/1.0",
    "RTSP/2.0"
]


def decode_type(pkt):
    content = pkt
    if len(content) == 0:
        return None
    else:
        lines = content.split(CRLF)
        first_line = lines[0].split(" ")
        if first_line[0] in METHOD:
            print("RTSP Request")
            return RTSP_Request(content)
        elif first_line[0].startswith("RTSP"):
            print("RTSP Response")
            return RTSP_Response(content)
        return None


class RTSP_Packets_Hanlder:
    def __init__(self, packets,sip,dip,sport,dport):
        self.sip=sip
        self.dip=dip
        self.sport=sport
        self.dport=dport
        self.raw_packets = packets
        self.packets = []
        self.decode_all()
        self.handle()

    def decode_all(self):
        old = None
        if old is None:
            current = decode_type(self.raw_packets)
            if current is not None and current.decode():
                self.packets.append(current)
                # print(self.packets)
                old = None
            else:
                old = current
        else:
            if old.more(rtsp_pkt):
                self.packets.append(old)
                old = None

    def dml(self,sql):
        try:
            cursor.execute(sql)
            db.commit()
            print("数据操纵成功")
        except:
            print('数据操作出错啦')
            db.rollback()

    def handle_transport(self,transport):
        cport=None
        sport=None
        for x in transport:
            if x.startswith("client"):
                client_port = (x.split('=')[1]).split('-')
                rtp_port = int(client_port[0])  #rtp传输客户端端口
                rtcp_port = int(client_port[1])  #rtcp传输客户端端口
                cport = [rtp_port, rtcp_port]
            elif x.startswith("server"):
                server_port = (x.split('=')[1]).split('-')
                rtp_port = int(server_port[0])
                rtcp_port = int(server_port[1])
                sport = [rtp_port, rtcp_port]
        return cport,sport

    def handle(self):
        for pkt in self.packets:
            # print(pkt, "\n")
            if isinstance(pkt, RTSP_Request): #RTSP请求报文
                if pkt.method == "TEARDOWN":
                    print("收到会话结束命令，根据Session从表格中删除相关流会话信息，这里可以在数据可中设定触发器，删除数据的同时数据备份到另一个表格")
                    print((self.sip, self.dip, pkt.type_header['Session']))
                    sql = " delete from rtsp_tcptb where rtsp_tcptb.session='%s' " % \
                          (pkt.type_header['Session'])
                    self.dml(sql)
                    sql = "delete from rtsp_udptb where session='%s' " % \
                          (pkt.type_header['Session'])
                    self.dml(sql)
                if pkt.method=="PLAY":
                    print("？？？？？？捕获到play播放命令，检查播放命令的操作时间，若与恶意RTSP命令匹配，则认为是恶意的摄像头操作命令？？？？？？？？？？")

            elif isinstance(pkt, RTSP_Response): #RTSP响应报文
                if pkt.status_code == '200' and "Session" in pkt.type_header.keys():
                    if "Transport" in pkt.type_header.keys() and pkt.type_header['Transport'].startswith("RTP/AVP/TCP;"):  #该情况对应rtp/rtsp/tcp传输方式
                        print("捕获到setup回复命令，提取5元组(源IP、目的IP、源端口、目的端口、Session)")
                        # dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # print(self.sip, self.dip, self.sport, self.dport, pkt.type_header['Session'],dt)
                        sql = "insert ignore into rtsp_tcptb(sip,dip,sport,dport,session,starttime,endtime) values('%s','%s',%d,%d,'%s',current_timestamp,null)" % (
                            self.sip, self.dip, self.sport, self.dport, pkt.type_header['Session'])
                        self.dml(sql)
                        sql = "insert ignore into rtsp_tcptb(sip,dip,sport,dport,session,starttime,endtime) values('%s','%s',%d,%d,'%s',current_timestamp,null)" % (
                            self.dip, self.sip, self.dport, self.sport, pkt.type_header['Session'])
                        self.dml(sql)
                    elif "Transport" in pkt.type_header.keys() and pkt.type_header['Transport'].startswith("RTP/AVP;"): #该情况对应rtp/udp的传输方式，信令通过rtsp/tcp传输
                        print("捕获到SETUP回复命令，提取7元组")
                        # dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        sql = "insert ignore into rtsp_udptb(sip,dip,sport,dport,session,starttime,endtime) values('%s','%s',%d,%d,'%s',current_timestamp,null)" % (
                            self.sip, self.dip, self.sport, self.dport, pkt.type_header['Session']) #'insert ignore into' 如果数据主键存在则忽略此次插入数据
                        self.dml(sql)
                        # sql = "insert ignore into rtsp_udptb(sip,dip,sport,dport,session,starttime,endtime) values('%s','%s',%d,%d,'%s',current_timestamp,null)" % (
                        #     self.dip, self.sip, self.dport, self.sport, pkt.type_header['Session'])  # 'insert ignore into' 如果数据主键存在则忽略此次插入数据
                        # self.dml(sql)
                        transport=pkt.type_header['Transport'].split(';')
                        client_port,server_port=self.handle_transport(transport)
                        sql="select client_port,server_port from rtsp_udptb where rtsp_udptb.sip='%s' and rtsp_udptb.dip='%s' and rtsp_udptb.sport='%s' and rtsp_udptb.dport='%s' and rtsp_udptb.session='%s'" % \
                            (self.sip, self.dip, self.sport, self.dport, pkt.type_header['Session'])
                        cursor.execute(sql)
                        result=cursor.fetchone()
                        if result[0] != None and result[1] != None:
                            # print(result)
                            cport = eval(result[0])  #将字符转换成列表
                            sport = eval(result[1])
                            if client_port != cport:
                                client_port = client_port + cport
                                client_port = sorted(set(client_port), key=client_port.index) #去除重复端口，并按原来的顺序不变
                            if server_port != sport:
                                server_port = server_port + sport
                                server_port = sorted(set(server_port), key=server_port.index) #去除重复端口，并按原来的顺序不变
                            # print(client_port, server_port)
                        sql = "update rtsp_udptb set client_port='%s',server_port='%s' where sip='%s' and dip='%s' and sport='%s' and dport='%s' and session='%s'" % \
                              (client_port, server_port, self.sip, self.dip, self.sport, self.dport,pkt.type_header['Session'])
                        self.dml(sql)

                elif pkt.status_code == '401':
                    print("Response status=", pkt.status_code, "Response reason_phrase=", pkt.reason_phrase)
                    print("？？？？？？？？？？这里需要记录通一会话中摄像头验证失败的次数，由此识别字典攻击？？？？？？？？？？")


# 从嗅探的流中识别rtsp协议
def isRTSP(tcppayload):
    content = tcppayload
    try:
        lines = content.split(" ")
        if lines[0] in RTSP_fingerprints:
            # print("is rtsp")
            return True
    except:
        return False


