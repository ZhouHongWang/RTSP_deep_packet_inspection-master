#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from rtsphandle.utils import convert_bytes_to_str
from rtsphandle.rtspparser import *

import threading

rtptcp_count=0
rtpudp_count=0

def call_pro_select_tcpport(s_ip,d_ip,s_port,d_port):
    global rtptcp_count
    try:
        results = cursor.callproc('pro_select_tcpport', (s_ip, d_ip, s_port, d_port, 0))
        # print(results)
        if results[4] > 0:  # 返回结果大于0，说明有检索到对应ip和端口信息，将<SIP,DIP,SPORT,DPORT>传输的数据包全部聚合为一条流，主要包括RTP数据包和RTCP数据包
            rtptcp_count += 1
            print('rtptcp_count=', rtptcp_count)
            # return True
        else:
            print("TCP数据段，没有查询结果，即不是RTP TCP媒体流")
            # return False
    except Error as e:
        print("pro_select_tcpport error:",e)
        return False

def call_pro_select_udpport(s_ip, d_ip, s_port, d_port):
    global rtpudp_count
    find = 0
    try:
        # print('udp')
        cursor.callproc('pro_select_udpport', (s_ip, d_ip))
        results =cursor.stored_results()
        # print(results.fetchall())
        for re in results:
            values=re.fetchall()
            for x in values:
                select_port=eval(x[0])+eval(x[1])
                if s_port in select_port and d_port in select_port:
                    rtpudp_count += 1
                    print('rtpudp_count=', rtpudp_count)
                    find=1
                    break
        if find != 1:
            print("UDP数据报，没有查询结果，即不属于RTP UDP流媒体")
    except Error as e:
        print("pro_select_udpport error", e)

def callback(packet):
    if packet.haslayer('Ethernet'):
        if packet.haslayer('IP'):
            try:
                s_ip = packet['IP'].src
                d_ip = packet['IP'].dst
                if packet.haslayer('TCP'):
                    s_port = packet['TCP'].sport
                    d_port = packet['TCP'].dport
                    if len(packet['TCP'].payload) != 0:
                        tcppayload = convert_bytes_to_str(packet['TCP'].payload.load)
                        # print(tcppayload)
                        if tcppayload is None or len(tcppayload.strip(b'\x00'.decode(encoding='utf-8'))) == 0:
                            # 不是文本协议,或者文本协议的消息体中携带了二进制数据，比如HTTP协议的消息体中会携带二进制数据
                            # 看在RTSP TCP流级会话信息表中是否检索到ip和port信息，检索到则代表是rtp over rtsp over tcp播放方式的监控
                            # try:
                            #     results = cursor.callproc('pro_select_tcpport', (s_ip, d_ip, s_port, d_port, 0))
                            #     # print(results)
                            #     if results[4] > 0:
                            #         rtp_count += 1
                            #         print('rtp_count=', rtp_count)
                            # except Error as e:
                            #     print(e)
                            call_pro_select_tcpport(s_ip, d_ip, s_port, d_port)

                        else:  # 文本协议，RTSP\HTTP\FTP等
                            result = isRTSP(tcppayload)  # 经过rtsp指纹库判断是否是rtsp协议
                            if result:  # 结果是rtsp协议，进一步解析协议
                                RTSP_Packets_Hanlder(tcppayload, s_ip, d_ip, s_port, d_port)
                            else:
                                # 是文本协议，但不是RTSP协议
                                pass
                    else:
                        # TCP不带负载，比如TCP ACK报文
                        call_pro_select_tcpport(s_ip, d_ip, s_port, d_port)  # 将摄像头与客户端之间的ack报文也归类为RTP TCP媒体流
                elif packet.haslayer('UDP'):
                    # UDP报文，看在RTSP udp流级会话信息状态表是否能检索到ip和port，检索到则代表是rtp over udp方式播放的监控
                    s_port = packet['UDP'].sport
                    d_port = packet['UDP'].dport
                    call_pro_select_udpport(s_ip, d_ip, s_port, d_port)
                    # pass
                else:
                    print("传输层不是TCP也不是UDP")
            except:
                print('handling tcp or udp error')
                pass
        else:
            print('网络层使用的不是IP协议，可能是ARP或者ICMP')
    else:
        print("数据链路层使用的不是Ethernet II帧")

def sniffer(savefilename):
    packets=sniff(prn=callback)
    # wrpcap(savefilename,packets)

def test(stream):
    for packet in stream:
        # packet.show()
        if packet.haslayer('Ethernet'):
            if packet.haslayer('IP'):
                try:
                    s_ip = packet['IP'].src
                    d_ip = packet['IP'].dst
                    if packet.haslayer('TCP'):
                        s_port = packet['TCP'].sport
                        d_port = packet['TCP'].dport
                        if len(packet['TCP'].payload) != 0:
                            tcppayload = convert_bytes_to_str(packet['TCP'].payload.load)
                            # print(tcppayload)
                            if tcppayload is None or len(tcppayload.strip(b'\x00'.decode(encoding='utf-8'))) == 0:
                                # 不是文本协议,或者文本协议的消息体中携带了二进制数据，比如HTTP协议的消息体中会携带二进制数据
                                # 看在RTSP TCP流级会话信息表中是否检索到ip和port信息，检索到则代表是rtp over rtsp over tcp播放方式的监控
                                # try:
                                #     results = cursor.callproc('pro_select_tcpport', (s_ip, d_ip, s_port, d_port, 0))
                                #     # print(results)
                                #     if results[4] > 0:
                                #         rtp_count += 1
                                #         print('rtp_count=', rtp_count)
                                # except Error as e:
                                #     print(e)
                                call_pro_select_tcpport(s_ip, d_ip, s_port, d_port)

                            else:  # 文本协议，RTSP\HTTP\FTP等
                                result = isRTSP(tcppayload)  # 经过rtsp指纹库判断是否是rtsp协议
                                if result:  # 结果是rtsp协议，进一步解析协议
                                    RTSP_Packets_Hanlder(tcppayload, s_ip, d_ip, s_port, d_port)
                                else:
                                    # 是文本协议，但不是RTSP协议
                                    pass
                        else:
                            # TCP不带负载，比如TCP ACK报文
                            call_pro_select_tcpport(s_ip, d_ip, s_port, d_port)  # 将摄像头与客户端之间的ack报文也归类为RTP TCP媒体流
                    elif packet.haslayer('UDP'):
                        # UDP报文，看在RTSP udp流级会话信息状态表是否能检索到ip和port，检索到则代表是rtp over udp方式播放的监控
                        s_port = packet['UDP'].sport
                        d_port = packet['UDP'].dport
                        call_pro_select_udpport(s_ip, d_ip, s_port, d_port)
                        # pass
                    else:
                        print("传输层不是TCP也不是UDP")
                except:
                    print('handling tcp or udp error')
                    pass
            else:
                print('网络层使用的不是IP协议，可能是ARP或者ICMP')
        else:
            print("数据链路层使用的不是Ethernet II帧")

def read_file(file):
    stream = rdpcap(file)
    return stream

if __name__ == '__main__':
    # file=r'D:\Code\PycharmCode\网络流量分析\IPC\数据集\row\RTSP_RTP_udp.pcap'
    file = r'D:\Code\PycharmCode\网络流量分析\IPC\数据集\row\RTSP_RTP_TCP.pcap'
    # stream = read_file(file)
    # test(stream)
    savefilename=r'rtsppasertest.pcap'
    sniffer(savefilename)
