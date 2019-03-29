import socket
import ssl
import re
import json


def read_line(s):
    buffer = b""
    while True:
        buf = s.recv(1, 0)
        buffer += buf
        last_two_bytes = buffer[-2:]
        if last_two_bytes == b"\r\n":
            break
    return buffer


def read_bytes(s, size):
    buffer = b""
    size_ = size
    while size_ != 0:
        buf = s.recv(size_, 0)
        buffer += buf
        # caculate remain bytes
        size_ -= len(buf)
    return buffer


kw = "test"
server_addr = ("fanyi.baidu.com", 443)

# make socket
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

# warp socket
ssl_sk = ssl.wrap_socket(sk)

# connect
ssl_sk.connect(server_addr)
# send request
str_request = "POST /sug HTTP/1.1\r\n"
str_request += f"Host: {server_addr[0]}\r\n"
str_request += "Accept: application/json, text/javascript, */*; q=0.01\r\n"
str_request += "Content-Type: application/x-www-form-urlencoded; charset=UTF-8\r\n"
str_request += "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36\r\n"
str_request += "Connection: Close\r\n"
str_request += "Content-Length: "+str(len(kw)+3)+"\r\n"
# str_request += "Cookie: \r\n"
str_request += "\r\n"
str_request += "kw="+kw

ssl_sk.send(str_request.encode("utf-8"), 0)
# recive data
# check if packed
# convert to dict

buf_header = b""
while True:
    buf = ssl_sk.recv(1, 0)
    buf_header += buf
    last_four_byte = buf_header[-4:]
    if last_four_byte == b"\r\n\r\n":
        print("Head Complete")
        break

# analyze head
str_header = buf_header.decode("utf-8")
# print(str_header)

# get chunked
regexp = r"Transfer-Encoding: (.*)\r\n"
result = re.findall(regexp, str_header, re.MULTILINE)
if result and result[0] == "chunked":
    print("分包")
    buf_content = b""
    len_package = -1
    while len_package != 0:
        buf_line = read_line(ssl_sk)
        str_line = buf_line[:-2].decode("utf-8")
        print(str_line)
        len_package = int(str_line, 16)
        buffer = read_bytes(ssl_sk, len_package)
        buf_content += buffer
        read_bytes(ssl_sk, 2)

    print(buf_content.decode("unicode_escape"))
    json_content = json.loads(buf_content)
    # json_content = json.loads(b"{\""+buf_content)
    if json_content["errno"]==0:
        print("Translate OK")
        print(json_content["data"][0]["v"])

else:
    print("非分包")
