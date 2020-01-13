import dpkt

RTSP_PORT = 554

CRLF = "\r\n"

TYPE_REQUEST = 1
TYPE_RESPONSE = 2

#RTSP头部域

# 通用头部：通用标头是可以在请求和响应中使用的标头
GENERAL_HEADERS = [
    "Cache-Control",
    "Connection",
    "CSeq",
    "Cseq",
    "Date",
    "Via",
    "Accept-Ranges",
    "Media-Properties",
    "Media-Range",
    "Pipelined-Requests",
    "Proxy-Supported",
    "Range","RTP-Info",
    "Scale","Seek-Style",
    "Server","Session",
    "Speed",
    "Supported",
    "Timestamp",
    "Transport",
    "User-Agent",
    "Via"
]

#方法
METHOD = [
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
    "TEARDOWN"
]

# 请求头部
REQUEST_HEADERS = [
    "Accept",
    "Accept-Credentials",
    "Accept-Encoding",
    "Accept-Language",
    "Authorization",
    "Bandwidth",
    "Blocksize",
    "Conference",
    "From",
    "If-Match",
    "If-Modified-Since",
    "If-None-Match",
    "Notify-Reason",
    "Proxy-Authorization",
    "Proxy-Require",
    "Range",
    "Referer",
    "Require",
    "Scale",
    "Session",
    "Speed",
    "Request-Status",
    "Transport",
    "User-Agent",
    "Terminate-Reason"
]

# 响应头部
RESPONSE_HEADERS = [
    "Content-Type",
    "Public",
    "Range",
    "Retry-After",
    "RTP-Info",
    "Scale",
    "Session",
    "Server",
    "Speed",
    "Transport",
    "Unsupported",
    "WWW-Authenticate",
    "Vary","Location",
    "Authentication-Info",
    "Connection-Credentials",
    " MTag",
    "Proxy-Authenticate"
]

# 实体头部
ENTITY_HEADERS = [
    "Allow",
    "Content-Base",
    "Content-Encoding",
    "Content-Language",
    "Content-Length",
    "Content-Location",
    "Content-Type",
    "Expires",
    "Last-Modified"
]

class RTSP:

    def __init__(self, raw, type=TYPE_REQUEST):
        self.type = type
        self.raw = raw
        self.version = None

        self.general_header = {}
        self.type_header = {}
        self.entity_header = {}
        self.others_header = {}

        self.content = ''
        self.nb_packets = 1

    def decode(self):
        lines = self.raw.split(CRLF)

        self.decode_first_line(lines.pop(0))

        while len(lines) > 0:
            line = lines.pop(0)
            splitted = line.split(": ")
            if len(line) == 0 and len(lines) > 0 and "Content-Length" in self.entity_header:
                self.content = CRLF.join(lines)
                if len(self.content) < int(self.entity_header["Content-Length"]):
                    return False
                else:
                    return True
            if len(splitted) is not 2:
                continue
            if self.type == TYPE_REQUEST and splitted[0] in REQUEST_HEADERS:
                self.type_header[splitted[0]] = splitted[1]
            elif self.type == TYPE_RESPONSE and splitted[0] in RESPONSE_HEADERS:
                self.type_header[splitted[0]] = splitted[1]
            elif splitted[0] in ENTITY_HEADERS:
                self.entity_header[splitted[0]] = splitted[1]
            elif splitted[0] in GENERAL_HEADERS:
                self.general_header[splitted[0]] = splitted[1]
            else:
                self.others_header[splitted[0]] = splitted[1]
        return True

    def decode_first_line(self, line):
        return None

    def more(self, content):
        self.content = self.content + content
        self.nb_packets += 1
        if len(self.content) < int(self.entity_header["Content-Length"]):
            return False
        return True

    def str_general_header(self):
        if len(self.general_header) == 0:
            return ''
        s = "[ GENERAL HEADER ]\n"
        for k, v in self.general_header.items():
            s += k + ": " + v + "\n"
        return s + "\n"

    def str_type_header(self):
        if len(self.type_header) == 0:
            return ''
        s = "[ REQUEST HEADER ]\n" if self.type == TYPE_REQUEST else "[ RESPONSE HEADER ]\n"
        for k, v in self.type_header.items():
            s += k + ": " + v + "\n"
        return s + "\n"

    def str_entity_header(self):
        if len(self.entity_header) == 0:
            return ''
        s = "[ ENTITY HEADER ]\n"
        for k, v in self.entity_header.items():
            s += k + ": " + v + "\n"
        return s + "\n"

    def str_others_header(self):
        if len(self.others_header) == 0:
            return ''
        s = "[ OTHERS HEADER ]\n"
        for k, v in self.others_header.items():
            s += k + ": " + v + "\n"
        return s + "\n"

    def str_content(self):
        if len(self.content) == 0:
            return ''
        s = "[ CONTENT ]\n" + self.content
        return s + "\n"

    def __str__(self):
        s = ''
        s += self.str_general_header()
        s += self.str_type_header()
        s += self.str_entity_header()
        s += self.str_others_header()
        s += self.str_content()
        return s


class RTSP_Request(RTSP):

    def __init__(self, raw):
        RTSP.__init__(self, raw, TYPE_REQUEST)
        self.method = None
        self.URI = None

    def decode_first_line(self, line):
        first_line = line.split(" ")
        self.method = first_line[0]
        self.URI = first_line[1]
        self.version = first_line[2]

    def __str__(self):
        s = "=============== RTSP REQUEST =============== (nb packets: " + str(self.nb_packets) +")\n"
        s += "method: " + self.method + "\n"
        s += "URI: " + self.URI + "\n"
        s += "version: " + self.version + "\n\n"
        return s + RTSP.__str__(self)

class RTSP_Response(RTSP):

    def __init__(self, raw):
        RTSP.__init__(self, raw, type=TYPE_RESPONSE)
        self.status_code = None
        self.reason_phrase = None

    def decode_first_line(self, line):
        first_line = line.split(" ")
        self.version = first_line[0]
        self.status_code = first_line[1]
        self.reason_phrase = first_line[2]

    def __str__(self):
        s = "=============== RTSP RESPONSE =============== (nb packets: " + str(self.nb_packets) +")\n"
        s += "version: " + self.version + "\n"
        s += "status code: " + self.status_code + "\n"
        s += "reason phrase: " + self.reason_phrase + "\n\n"
        return  s + RTSP.__str__(self)