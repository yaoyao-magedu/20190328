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


server_addr = ("ke.qq.com", 443)

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
str_request += "\r\n"

ssl_sk.send(str_request.encode("utf-8"), 0)

buf_header = b""
while True:
    buf = ssl_sk.recv(1, 0)
    buf_header += buf
    last_four_byte = buf_header[-4:]
    if last_four_byte == b"\r\n\r\n":
        # print("Head Complete")
        break

# analyze head
str_header = buf_header.decode("utf-8")
# print(str_header)

# # get Content-Length
regexp = r"Content-Length: (\d*?)\r\n"
str_len = re.findall(regexp, str_header, re.MULTILINE)
if str_len:
    int_len = int(str_len[0], 10)
    print("数据大小: ", int_len)
    # read body
    buffer = read_bytes(ssl_sk, int_len)
    print(buffer.decode("utf-8"))
else:
    print("分包")
