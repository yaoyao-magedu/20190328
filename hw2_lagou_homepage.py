import socket
import ssl
import re


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

def read_block(s, size):
    buffer = b""
    size_ = size
    while size_ != 0:
        buf = s.recv(size_, 0)
        buffer += buf
        # caculate remain bytes
        size_ -= len(buf)
    return buffer

server_addr = ("www.lagou.com", 443)

# create socket
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
# warp socket
ssl_sk = ssl.wrap_socket(sk)
# connect https
ssl_sk.connect(server_addr)
# send request
str_request = "GET / HTTP/1.1\r\n"
str_request += f"Host: {server_addr[0]}\r\n"
str_request += "Accept: text/html,text/css,text/javascript\r\n"
str_request += "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36\r\n"
str_request += "Accept-Language: zh-cn\r\n"
str_request += "Connection: close\r\n"
# str_request += "Keep-Alive: 100\r\n"
str_request += "\r\n"

ssl_sk.send(str_request.encode("utf-8"), 0)

# get server response
#
# while True:
#     buf = ssl_sk.recv(4 * 1024, 0)
#     if not buf:
#         break
#     print(buf.decode())

# analyze data
# get head
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
print(result)
if result and result[0] == "chunked":
    print("分包")
    buf_content = b""
    len_package = -1
    while len_package != 0:
        buf_line = read_line(ssl_sk)
        str_line = buf_line[:-2].decode("utf-8")
        print(buf_line)
        len_package = int(str_line, 16)
        print(len_package)
        read_bytes(ssl_sk, 2)
        buffer = read_bytes(ssl_sk, len_package)
        buf_content += buffer

    print("Read End")
    print(buf_content.decode("utf-8"))
else:
    print("非分包")
