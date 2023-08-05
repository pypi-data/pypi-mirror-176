import socket
from time import sleep


if __name__=='__main__':

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('127.0.0.1',5421))
    s.listen()
    
    conn,addr=s.accept()
    while True:
        data=conn.recv(1024)
        if not data:
            break
        print(data)