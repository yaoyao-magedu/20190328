"""
Get Data from Youdao
"""
import socket
import ssl
import re
import json
from PyQt5.QtCore import QObject


class YoudaoTranslator(QObject):
    def __init__(self):
        super().__init__()
        # Request Head
        self.str_request = "POST /translate_o?smartresult=dict&smartresult=rule HTTP/1.1\r\n"
        self.str_request += "Host: fanyi.youdao.com\r\n"
        self.str_request += "Accept: application/json, text/javascript, */*; q=0.01\r\n"
        self.str_request += "Content-Type: application/x-www-form-urlencoded; charset=UTF-8\r\n"
        self.str_request += "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36\r\n"
        self.str_request += "Connection: Close\r\n"
        self.str_request += "Content-Length: {length}\r\n"
        self.str_request += "\r\n"
        self.str_request += "i={keyword}&from=AUTO&to=AUTO&doctype=json"

    def translate(self, kw):
        print("Start Translate Youdao", kw)

        # make socket
        sk_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

        # warp socket
        ssl_sk_ = ssl.wrap_socket(sk_)

        # connect
        ssl_sk_.connect(("fanyi.youdao.com", 443))
        # send request
        request = self.str_request.format(length=len(kw.encode())+2, keyword=kw)
        ssl_sk_.send(request.encode("utf-8"), 0)
        # read headers
        buf_header_ = self.__read_headers(ssl_sk_)
        # get checked
        str_header_ = buf_header_.decode("utf-8")
        print(str_header_)
        regexp = r"Content-Length: (\d*?)\r\n"
        re_ = re.findall(regexp, str_header_, re.M)
        buf_body = b""
        # read block
        if re_:
            print("非分包")
            len_body_ = int(re_[0], 10)
            buf_body += self.__read_block(ssl_sk_, len_body_)
            print("OK")
        else:
            len_block_ = -1
            while len_block_ != 0:
                line_ = self.__read_line(ssl_sk_)
                len_block_ = int(line_[:-2].decode("utf-8"), 16)
                buf_body += self.__read_block(ssl_sk_, len_block_)
                self.__read_block(ssl_sk_,2)
            print("ok")
        print(buf_body)
        result = json.loads(buf_body)
        print(result)
        if result.get("errorcode", 1) == 0:
            result = result["data"][0]["v"]
            print(result)
        else:
            result = "ERROR"
        ssl_sk_.close()
        sk_.close()
        return result


    def __read_headers(self, s):
        buf_header = b""
        while True:
            buf = s.recv(1, 0)
            buf_header += buf
            last_four_byte = buf_header[-4:]
            if last_four_byte == b"\r\n\r\n":
                print("Head Complete")
                break
        return buf_header

    def __read_line(self, s):
        buffer = b""
        while True:
            buf = s.recv(1, 0)
            buffer += buf
            last_two_bytes = buffer[-2:]
            if last_two_bytes == b"\r\n":
                break
        return buffer

    def __read_block(self, s, size):
        buffer = b""
        size_ = size
        while size_ != 0:
            buf = s.recv(size_, 0)
            buffer += buf
            # caculate remain bytes
            size_ -= len(buf)
        return buffer

